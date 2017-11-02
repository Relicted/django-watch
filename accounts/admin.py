from django.contrib import admin
from .models import Profile, PasswordResetLink


admin.site.register(Profile)

admin.site.register(PasswordResetLink)