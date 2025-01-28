from django.contrib import admin
from django.urls import path,include
from .views import registration_view,verify_email, CustomLoginView,index_pg,ContactUsForm,auto_logout_view


urlpatterns = [
   path("accounts/", include("django.contrib.auth.urls")),
   path("", index_pg, name="index"),
   path("contact-us/",ContactUsForm, name="contact-us/"),
   path("accounts/register/",registration_view, name = "register"),
   path('accounts/verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
   path('login/', CustomLoginView.as_view(), name='login'),


   #autologout
   path('auto_logout/', auto_logout_view, name='auto_logout'),
]