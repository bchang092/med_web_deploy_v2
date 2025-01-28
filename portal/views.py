

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django import forms


User = get_user_model()




class ContactUsForm(forms.Form):
   email = forms.EmailField(label="Email",required=True)
   first_name = forms.CharField(required=True)
   last_name = forms.CharField(required=True)
   message= forms.CharField()
#home page
def index_pg(request):
   if request.method == "POST":
       form = ContactUsForm(request.POST)  # Use the form defined above
       if form.is_valid():
           # Extract the data from the form
           first_name = form.cleaned_data['first_name']
           last_name = form.cleaned_data['last_name']
           email = form.cleaned_data['email']
           message = form.cleaned_data['message']


           # Construct the email message
           email_message = f"First Name: {first_name}\n"
           email_message += f"Last Name: {last_name}\n"
           email_message += f"Email: {email}\n\n"
           email_message += f"Message:\n{message}"


           # Send the email
           subject = "Interest Form Submission"
           send_mail(subject, email_message, 'awesometroller1234@gmail.com',
                     ['bchang092@gmail.com'])


           # After submitting, redirect to avoid resubmission on refresh
           return redirect('index')
   else:
       form = ContactUsForm()  # Initialize the form for GET request


   return render(request, "index.html", {"form": form})


def auto_logout_view(request):
   from django.contrib.auth import logout


   # Log the user out automatically
   logout(request)
   return redirect('index') 


#registration view
def registration_view(request):
   if request.method == "POST":
       form = RegistrationForm(request.POST)
       if form.is_valid():
           user = form.save()
           # Create a user profile and set is_verified to False by default


           # Verification token generation
           token = default_token_generator.make_token(user)
           uid = urlsafe_base64_encode(force_bytes(user.pk))
           verification_url = reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
           verification_link = f"http://{request.get_host()}{verification_url}"


           subject = "Verify your email address"
           message = render_to_string('registration/verification_email.txt', {
               'user': user,
               'verification_url': verification_link,
           })
           html_message = render_to_string('registration/verification_email.html', {
               'user': user,
               'verification_url': verification_link,
           })
           send_mail(subject, message, 'awesometroller1234@gmail.com',
                     [user.email], html_message=html_message,)


           return HttpResponse("Please check your email to verify your account.")
      
   else:
       form = RegistrationForm()


   return render(request,"registration/register.html", {"form":form})


#verify email view
def verify_email(request, uidb64, token):
   try:
       uid = force_str(urlsafe_base64_decode(uidb64))
       user = User.objects.get(pk=uid)
   except (TypeError, ValueError, OverflowError, User.DoesNotExist):
       user = None


   if user is not None and default_token_generator.check_token(user, token):
       user.is_verified = True  # Activate user after email verification
       user.save()


       return render(request,'registration/verify_email_success.html')
   else:
       return HttpResponse("Invalid or expired verification link!")




#login - note: don't allow login if is_verified is false
class CustomLoginView(LoginView):
   #clear residual messages:
   def get(self, request, *args, **kwargs):
       # Clear any messages that might have been carried over
       storage = messages.get_messages(request)
       storage.used = True
       return super().get(request, *args, **kwargs)
  
   def form_valid(self, form):
       # Check if the user is verified
       user = form.get_user()
       if not user.is_verified:
           messages.error(self.request, "Please verify your email before logging in.")
           return redirect('login')  # Redirect back to the login page
      
       # Proceed with the default behavior if verified
       return super().form_valid(form)


   #define where to reroute a successful login
   def get_success_url(self):
       # Check the user's role and redirect accordingly
       user = self.request.user
       if user.role == 'admin':
           return '/reviews/admin_home/'  # Redirect to admin page
       elif user.role == 'volunteer':
           return '/reviews/volunteer_home/'  # Redirect to volunteer home page
       else:
           return '/'  # Default redirect (you can change this if needed)
def index(request):
   return render(request,"index.html")

