from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from datetime import timedelta
from .models import UserSessionToken,ActivityLog
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import re

def login_view(request):
    if request.method=="POST":
        login_input=request.POST.get("login_input")
        password=request.POST.get("password")
        remenber_me=request.POST.get("remember_me")

        print("LOGIN INPUT:",login_input)
        print("PASSWORD:",password)

        
        try:
                user_obj=User.objects.get(email__iexact=login_input)
                username=user_obj.username
        except User.DoesNotExist:
                username=login_input
        print("USERNAME USED:",username)
        user=authenticate(request,username=username,password=password)
        print("AUTH USER:", user)
        if user is not None:
            login(request,user)

            ActivityLog.objects.create(
                 user=user,
                 action="Logged In"
            )
            if not remenber_me:
                 request.session.set_expiry(0)

            refresh= RefreshToken.for_user(user)
            access_token=str(refresh.access_token)
            refresh_token=str(refresh)
            expires_at=now()+timedelta(minutes=1)

            token_record=UserSessionToken.objects.create(
                user=user,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=expires_at,

            )
            request.session["session_id"]=str(token_record.session_id)
            role= user.userprofile.role

            if role =="admin":
                return redirect("admin_dashboard")
            elif role=="manager":
                return redirect("manager_dashboard")
            elif role=="tester":
                return redirect("tester_dashboard")
            else:
                return render(request,"accounts/login.html",
                              {"error": "User role is not assigned"})
    return render(request,"accounts/login.html")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "Token is valid. You can access this protected page."})

@login_required
def admin_dashboard(request):
    if request.user.userprofile.role !="admin":
         return HttpResponse("Access Denied")
    return render(request,"accounts/admin_dashboard.html",{"session_id":request.session.get("session_id")})

@login_required
def manager_dashboard(request):
    if request.user.userprofile.role !="manager":
         return HttpResponse("Access Denied")
    return render(request,"accounts/manager_dashboard.html",{"session_id":request.session.get("session_id")})

@login_required
def tester_dashboard(request):
    if request.user.userprofile.role !="tester":
         return HttpResponse("Access Denied")
    return render(request,"accounts/tester_dashboard.html",{"session_id":request.session.get("session_id")})


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])

def refresh_session_token(request):
    session_id= request.data.get("session_id")

    try:
        old_token=UserSessionToken.objects.filter(session_id=session_id).latest("created_at")
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
    
def logout_view(request):
     logout(request)
     return redirect("login")

def forgot_password_view(request):
     if request.method=="POST":
          email=request.POST.get("email")

          user=User.objects.filter(email=email).first()

          if user:
               request.session["reset_user_id"]=user.id
               return redirect("reset_password")
          else:
               return render(request, "accounts/forgot_password.html",{"error": "Email not found"})
    
     return render(request,"accounts/forgot_password.html") 

def is_valid_password(password):
     if len(password)<8:
          return False
     if not re.search(r"[A-Z]",password):
          return False
     if not re.search(r"[a-z]",password):
          return False
     if not re.search(r"[0-9]",password):
          return False
     if not re.search(r"[!@$%*?&]",password):
          return False
     return True
     
    

def reset_password_view(request):
     if request.method=="POST":
          user_id=request.session.get("reset_user_id")
          new_password=request.POST.get("new_password")
          confirm_password=request.POST.get("confirm_password")
          if not is_valid_password(new_password):
            return render(request, "accounts/reset_password.html", {
        "error": "Password must be at least 8 characters and include 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special symbol."
    })

          if new_password!= confirm_password:
               return render(request, "accounts/reset_password.html",{"error":"Passwords do not match"})
          user=User.objects.get(id=user_id)
          user.set_password(new_password)
          user.save()

          del request.session["reset_user_id"]
          return redirect("login")

     return render(request,"accounts/reset_password.html")

def forgot_username_view(request):
     if request.method=="POST":
          email=request.POST.get("email")
          user=User.objects.filter(email=email).first()
          if user:
               return render(request,"accounts/forgot_username.html", {"username": user.username})
          else:
               return render(request,"accounts/forgot_username.html", {"error": "Email not found"})
     return render(request,"accounts/forgot_username.html")


@login_required
def change_password_view(request):
     if request.method=="POST":
          old_password=request.POST.get("old_password")
          new_password=request.POST.get("new_password")
          confirm_password=request.POST.get("confirm_password")

          if not request.user.check_password(old_password):
               return render(request,"accounts/change_password.html",{"error":"Old password is incorrect"})
          if new_password != confirm_password:
               return render(request,"accounts/change_password.html",{"error":"Passwords do not match"})
          if not is_valid_password(new_password):
               return render(request,"accounts/change_password.html",{"error":"Password must be at least 8 "
               "characters and include 1 uppercase letter,1 lowercase letter,1 number, and 1 special symbol."})
          request.user.set_password(new_password)
          request.user.save()

          return render(request,"accounts/change_password.html",{"success":"Password changed successfully"})
     return render(request,"accounts/change_password.html")

@login_required
def my_sessions_view(request):
     sessions=UserSessionToken.objects.filter(user=request.user).order_by("-created_at")
     return render(request,"accounts/my_sessions.html",{"sessions":sessions})