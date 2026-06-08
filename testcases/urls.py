from django.urls import path
from . import views

urlpatterns = [
    path("upload/",views.upload_testcase,name="upload_testcase"),
    path("list/",views.view_testcases,name="view_testcases"),
    path("update-status/<int:testcase_id>/",views.update_testcase_status,name="update_testcase_status"),
]