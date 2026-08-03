from django.shortcuts import render,redirect,get_object_or_404
from .forms import TestCaseForm
from django.contrib.auth.decorators import login_required
from .models import TestCase
from django.http import HttpResponse
from accounts.models import ActivityLog
from django.contrib import messages

@login_required
@login_required
def upload_testcase(request):
    if request.method == "POST":
        form = TestCaseForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data["title"]
            project_name = form.cleaned_data["project_name"]

            if TestCase.objects.filter(
                title__iexact=title,
                project_name__iexact=project_name,
            ).exists():
                messages.error(
                    request,
                    "A test case with this title already exists for this project.",
                )
                return render(
                    request,
                    "testcases/upload_testcase.html",
                    {"form": form},
                )

            testcase = form.save(commit=False)
            testcase.uploaded_by = request.user
            testcase.save()

            messages.success(
                request,
                "Test case uploaded successfully.",
            )

            return redirect("tester_dashboard")

    else:
        form = TestCaseForm()

    return render(
        request,
        "testcases/upload_testcase.html",
        {"form": form},
    )

@login_required
def view_testcases(request):
    testcases=TestCase.objects.all().order_by("-uploaded_at")
    return render(request,"testcases/view_testcases.html",{"testcases":testcases})

@login_required
def update_testcase_status(request,testcase_id):
    if request.user.userprofile.role != "manager":
        return HttpResponse("Access Denied")
    testcase=get_object_or_404(TestCase,id=testcase_id)
    if request.method=="POST":
        new_status=request.POST.get("status")
        testcase.status=new_status
        testcase.save()

        ActivityLog.objects.create(
            user=request.user,
            action=f"Updated {testcase.title} to {new_status}"
    )

    return redirect("view_testcases")



