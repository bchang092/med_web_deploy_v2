from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    #attribute notes: if volunteer gets deleted, cascade deletes all reviews
    Rating = models.IntegerField(help_text = "(1-10)", validators = [MinValueValidator(1), MaxValueValidator(10)],null=True,editable = True)
    vol_ID = models.IntegerField(help_text = "(Volunteer ID)",editable = True,null=True) 
    Department = models.CharField(max_length = 255, help_text = 'Department',editable = True)
    Review_Content = models.TextField(help_text="Your Review",editable = True)  # Store the review content (text)
    Date_Submitted = models.DateTimeField(auto_now_add=True,editable = True)  # Automatically set the current date/time when the review is created

    #admin username  (filtering feature)
    admin_user = models.CharField(max_length = 255)

    #sentiment analysis 
    Sentiment = models.TextField(editable = False)
    Volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews',editable = True)  # one to many relationship: one user can make many reviews
    Volunteer_First_Name = models.CharField(max_length=50, editable=False, null=True, blank = True)
    Volunteer_Last_Name = models.CharField(max_length=50, editable=False, null=True, blank = True)
    
    #admin response attribute to review
    Admin_Response = models.TextField(blank=True, null=True)  # New field

    #return url to particular review 
    def get_absolute_url(self):
        return reverse('review-details', args=[str(self.id)])
    
    #returns string representing review object
    def __str__(self):
        return f'{self.Department}, {self.Rating}, {self.Date_Submitted}' 
    
    class Meta:
        ordering = ['Date_Submitted','-Rating']

        #these permissions can be later defined in admin
        permissions = [('can_create_review','Can create a review'),
                       ('can_edit_review','Can edit a review'),
                        ('can_view_review','Can view reviews')]

   