from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.login_view, name="login"),
    path("protected/", views.protected_view,name="protected"),
    path("admin-dashboard/", views.admin_dashboard,name="admin_dashboard"),
    path("manager-dashboard/", views.manager_dashboard,name="manager_dashboard"),
    path("tester-dashboard/", views.tester_dashboard,name="tester_dashboard"),
    path("refresh-session-token/", views.refresh_session_token,name="refresh_session_token"),
    path("logout/",views.logout_view,name="logout"),
    path("forgot-password/",auth_views.PasswordResetView.as_view(
        template_name="accounts/forgot_password.html",
        email_template_name="accounts/password_reset_email.html",
        subject_template_name="accounts/password_reset_subject.txt",
        success_url="/password-reset-done/",),
        name="forgot_password",),
    path("password-reset-done/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done",),

    path("reset-password/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="accounts/reset_password.html",success_url="/password-reset-complete/",),name="password_reset_confirm",),

    path("password-reset-complete/",auth_views.PasswordResetCompleteView.as_view( template_name="accounts/password_reset_complete.html"),name="password_reset_complete",),
    path("change-password/",auth_views.PasswordChangeView.as_view(template_name="accounts/change_password.html"),name="change_password",),
    path("password-change-done/",auth_views.PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"),name="password_change_done",),
    path("my-sessions/",views.my_sessions_view,name="my_sessions"),
    path("forgot-username/",views.forgot_username_view,name="forgot_username"),

]
