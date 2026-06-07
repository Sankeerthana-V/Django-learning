from django import forms
from .models import TestCase

class TestCaseForm(forms.ModelForm):
    class Meta:
        model=TestCase
        fields=["title","project_name","description","status","uploaded_file"]