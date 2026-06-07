from django.db import models
from django.contrib.auth.models import User

class TestCase(models.Model):
    title= models.CharField(max_length=100)
    project_name= models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    STATUS_CHOICES=[
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Passed", "Passed"),
        ("Failed", "Failed"),
    ]
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="Pending")
    uploaded_file=models.FileField(upload_to="testcase_files/")
    uploaded_by=models.ForeignKey(User,on_delete=models.CASCADE)
    uploaded_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title