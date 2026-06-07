from django.contrib import admin
from .models import UserProfile, UserSessionToken

admin.site.register(UserProfile)
admin.site.register(UserSessionToken)
