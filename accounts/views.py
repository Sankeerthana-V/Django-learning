from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)

            if user.username=="admin":
                return HttpResponse("Welcome Admin")
            elif user.username=="manager1":
                return HttpResponse("Welcome Manager")
            elif user.username=="tester1":
                return HttpResponse("Welcome Tester")
            else:
                return render(request,"accounts/login.html",
                              {"error": "Invalid username or password"})
    return render(request,"accounts/login.html")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "Token is valid. You can access this protected page."})



