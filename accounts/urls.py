from django.urls import path
from . import views

urlpatterns = [
    path("",views.login_view, name="login"),
    path("protected/", views.protected_view,name="protected"),
]
