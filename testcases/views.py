from django.shortcuts import render,redirect
from .forms import TestCaseForm
from django.contrib.auth.decorators import login_required
from .models import TestCase

@login_required
def upload_testcase(request):
    if request.method=="POST":
        form=TestCaseForm(request.POST,request.FILES)

        if form.is_valid():
            testcase= form.save(commit=False)
            testcase.uploaded_by= request.user
            testcase.save()

            return redirect("tester_dashboard")
        
    else:
        form= TestCaseForm()
    return render(request,"testcases/upload_testcase.html",{"form":form})

@login_required
def view_testcases(request):
    testcases=TestCase.objects.all().order_by("-uploaded_at")
    return render(request,"testcases/view_testcases.html",{"testcases":testcases})




