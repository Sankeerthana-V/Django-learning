from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import SessionAuthentication
from django.utils.timezone import now
from datetime import timedelta
from .models import UserSessionToken,ActivityLog
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def login_view(request):
    if request.method == "POST":
        login_input = request.POST.get("login_input")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        try:
            user_obj = User.objects.get(email__iexact=login_input)
            username = user_obj.username
        except User.DoesNotExist:
            username = login_input

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:
            return render(
                request,
                "accounts/login.html",
                {
                    "error": "Invalid username/email or password."
                },
            )

        login(request, user)

        ActivityLog.objects.create(
            user=user,
            action="Logged In",
        )

        if not remember_me:
            request.session.set_expiry(0)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        expires_at = now() + timedelta(minutes=1)

        token_record = UserSessionToken.objects.create(
            user=user,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
        )

        request.session["session_id"] = str(
            token_record.session_id
        )

        role = user.userprofile.role

        if role == "admin":
            return redirect("admin_dashboard")

        if role == "manager":
            return redirect("manager_dashboard")

        if role == "tester":
            return redirect("tester_dashboard")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "User role is not assigned."
            },
        )

    return render(
        request,
        "accounts/login.html",
    )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "Token is valid. You can access this protected page."})

@login_required
@ensure_csrf_cookie
def admin_dashboard(request):
    if request.user.userprofile.role !="admin":
         return HttpResponse("Access Denied")
    return render(request,"accounts/admin_dashboard.html",{"session_id":request.session.get("session_id")})

@login_required
@ensure_csrf_cookie
def manager_dashboard(request):
    if request.user.userprofile.role !="manager":
         return HttpResponse("Access Denied")
    return render(request,"accounts/manager_dashboard.html",{"session_id":request.session.get("session_id")})

@login_required
@ensure_csrf_cookie
def tester_dashboard(request):
    if request.user.userprofile.role !="tester":
         return HttpResponse("Access Denied")
    return render(request,"accounts/tester_dashboard.html",{"session_id":request.session.get("session_id")})


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])

def refresh_session_token(request):
    session_id= request.data.get("session_id")

    try:
        old_token=UserSessionToken.objects.filter(session_id=session_id,user=request.user,).latest("created_at")
        refresh=RefreshToken(old_token.refresh_token)
        new_access_token=str(refresh.access_token)
        expires_at=now() + timedelta(minutes=1)

        UserSessionToken.objects.create(
            session_id=old_token.session_id,
            user=old_token.user,
            access_token=new_access_token,
            refresh_token=old_token.refresh_token,
            expires_at=expires_at,
        )

        return Response({
            "message":"New access token generated",
            "session_id":str(old_token.session_id),
            "access_token": new_access_token,
            "expires_at": expires_at

        })
    except Exception as e:
        return Response({
            "error": str(e)
        },status=400)

@login_required    
def logout_view(request):
     session_id=request.session.get("session_id")
     if session_id:
         UserSessionToken.objects.filter(
             session_id=session_id,
             user=request.user,
         ).delete()
         
     logout(request)
     return redirect("login")  


def forgot_username_view(request):
    message = None

    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            send_mail(
                subject="Your QA Automation Platform username",
                message=f"Your username is: {user.username}",
                from_email=None,
                recipient_list=[user.email],
            )

        message = (
            "If an account with this email exists, "
            "the username has been sent."
        )

    return render(
        request,
        "accounts/forgot_username.html",
        {"message": message},
    )


@login_required
def my_sessions_view(request):
     sessions=UserSessionToken.objects.filter(user=request.user).order_by("-created_at")
     return render(request,"accounts/my_sessions.html",{"sessions":sessions})