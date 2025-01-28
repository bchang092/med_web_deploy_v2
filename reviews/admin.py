from django.contrib import admin
from django.urls import path
from .models import Review
from django.contrib.auth.admin import UserAdmin


class AdminReviews(admin.ModelAdmin):
    list_display = ('Volunteer','admin_user','vol_ID','Date_Submitted','Department','Rating','Sentiment','Review_Content','Admin_Response')
    list_filter = ('Department', 'vol_ID','Date_Submitted')
    ordering = ('-Date_Submitted',)  # Default sorting (newest first)
    list_per_page = 20  # Show 20 reviews per page

admin.site.register(Review, AdminReviews)

