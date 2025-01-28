from django.contrib import admin
from django.urls import path
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class UserAdmin(admin.ModelAdmin):
    list_display = ('email','role','is_verified','first_name','last_name','date_reg')
    list_filter = ('role', 'is_verified','date_reg')
    ordering = ('-date_reg',)  # Default sorting (newest first)
    list_per_page = 20  # Show 20 reviews per page

admin.site.register(CustomUser, UserAdmin)
