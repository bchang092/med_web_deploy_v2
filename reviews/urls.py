from django.contrib import admin
from django.urls import path,include
from .views import volunteer_page, volunteer_form, volunteer_stats,edit_review,delete_reviews,admin_home,admin_review_view,admin_analysis,update_review,delete_review

urlpatterns = [
    #volunteer paths
    path("volunteer_home/", volunteer_page,name ="volunteer_home"),
    path("volunteer_stats/", volunteer_stats,name ="volunteer_stats"),
    path("volunteer_form/", volunteer_form,name ="volunteer_form"),

    #editing/deleting reviews
    path('review/edit/<int:id>/', edit_review, name='edit_review'),
    path('review/delete/<int:id>/', delete_review, name='delete_review'),

    #admin_view paths
    path('admin_home/',admin_home, name="admin_home"),
    path('admin_review_view/',admin_review_view, name="admin_review_view"),
    path('admin_analysis/',admin_analysis, name="admin_analysis"),

    #admin editing form 
    path('admin_review_view/update-review/', update_review, name='update-review'),
    path('delete-reviews/', delete_reviews, name='delete_reviews'),

]
