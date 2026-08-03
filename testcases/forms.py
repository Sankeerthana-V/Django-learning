from django import forms
from .models import TestCase


class TestCaseForm(forms.ModelForm):

    class Meta:
        model = TestCase
        fields = [
            "title",
            "project_name",
            "description",
            "uploaded_file",
        ]

    def clean_uploaded_file(self):
        file = self.cleaned_data.get("uploaded_file")

        if not file:
            return file

        allowed_extensions = [
            ".pdf",
            ".doc",
            ".docx",
            ".txt",
            ".xlsx",
            ".xls",
        ]

        extension = file.name.lower()

        if not any(extension.endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError(
                "Only PDF, DOC, DOCX, TXT, XLS and XLSX files are allowed."
            )

        max_size = 5 * 1024 * 1024  # 5 MB

        if file.size > max_size:
            raise forms.ValidationError(
                "File size must not exceed 5 MB."
            )

        return file