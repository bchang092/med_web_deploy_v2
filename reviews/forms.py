#form to handle review submission

from django import forms
from .models import Review
from django.core.validators import MinValueValidator, MaxValueValidator

class ReviewForm(forms.ModelForm):
    def clean_Rating(self):
        rating = self.cleaned_data.get('Rating')
        if rating < 1 or rating > 10:
            raise forms.ValidationError('Rating must be between 1 and 10.')
        return rating
    
    #clean the reviews to standardize them 
    def clean_Department(self):
        department = self.cleaned_data.get('Department')
        # Capitalize the first letter of each word in the department name
        standardized = ' '.join(word.capitalize() for word in department.split())
        return standardized
    
    def clean_admin_user(self):
        admin_username = self.cleaned_data.get('admin_user')
        from portal.models import CustomUser
        # Check if the username exists in the CustomUser model
        try:
            admin_user = CustomUser.objects.get(username=admin_username)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError(f"Admin user with username '{admin_username}' does not exist.")
        
        # Check if the user is an admin
        if admin_user.role != 'admin':
            raise forms.ValidationError(f"User '{admin_username}' is not an admin.")
        
        return admin_username

        
    class Meta:
        model = Review
        fields = ['Review_Content','Rating', 'Department','vol_ID','admin_user']  # Allow users to submit content for their review
        
        Rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        widget=forms.NumberInput(attrs={'min': 1, 'max': 10})
    )

        Review_Content = forms.CharField(
            label="Your Review",  # Custom label
            widget=forms.Textarea(attrs={'placeholder': 'Write your review here'})
        )

        Department = forms.CharField(
            label="Department You Worked In",  # Custom label
            widget=forms.TextInput(attrs={'placeholder': 'Enter department name'})
        )

        vol_ID = forms.IntegerField(
            label = "Volunteer ID",
            widget = forms.NumberInput()
        )


class edit_del_form(forms.ModelForm):
    def clean_Department(self):
        department = self.cleaned_data.get('Department')
        # Capitalize the first letter of each word in the department name
        standardized = ' '.join(word.capitalize() for word in department.split())
        return standardized
    
    class Meta:
        model = Review
        fields = ['Rating', 'Department', 'Review_Content','vol_ID']
        Rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        widget=forms.NumberInput(attrs={'min': 1, 'max': 10})
    )

        Review_Content = forms.CharField(
            label="Your Review",  # Custom label
            widget=forms.Textarea(attrs={'placeholder': 'Write your review here'})
        )

        Department = forms.CharField(
            label="Department You Worked In",  # Custom label
            widget=forms.TextInput(attrs={'placeholder': 'Enter department name'})
        )

        vol_ID = forms.IntegerField(
            label = "Volunteer ID",
            widget = forms.NumberInput()
        )
