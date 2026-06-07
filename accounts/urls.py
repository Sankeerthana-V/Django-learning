from django.urls import path
from . import views

urlpatterns = [
    path("",views.login_view, name="login"),
    path("protected/", views.protected_view,name="protected"),
    path("admin-dashboard/", views.admin_dashboard,name="admin_dashboard"),
    path("manager-dashboard/", views.manager_dashboard,name="manager_dashboard"),
    path("tester-dashboard/", views.tester_dashboard,name="tester_dashboard"),
    path("refresh-session-token/", views.refresh_session_token,name="refresh_session_token"),
    path("logout/",views.logout_view,name="logout"),
    path("forgot-password/",views.forgot_password_view,name="forgot_password"),
    path("reset-password/",views.reset_password_view,name="reset_password"),
    path("change-password/",views.change_password_view,name="change_password"),
    path("my-sessions/",views.my_sessions_view,name="my_sessions"),
    path("forgot-username/",views.forgot_username_view,name="forgot_username"),

]
