from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    role=models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class UserSessionToken(models.Model):
    session_id=models.UUIDField(default=uuid.uuid4,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    access_token=models.TextField()
    refresh_token=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    expires_at=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.session_id}"
    
class ActivityLog(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    action=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.action}"