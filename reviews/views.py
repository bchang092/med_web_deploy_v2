from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from django.db.models import Count
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
import pandas as pd 
import numpy as np 
# to get average of reviews per month 
from django.db.models import Avg
from django.db.models.functions import TruncMonth
from datetime import timedelta
from django.utils import timezone
from django.db.models import Min

#admin editing 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Sentiment analysis using RoBERTa model
import os
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification


################################## Volunteer Pages ##################################
#helper function to verify that correct admin/volunteer attributes 
def helper_verify(request):
    # Check if the logged-in user is a Volunteer
    if not hasattr(request.user, 'role') or request.user.role != 'volunteer':
        logout(request) #logout
        messages.error(request, "You are not authorized to access this page.")
        login_url = reverse('login')
        return redirect(login_url)  # Redirect to login or another page
    
@login_required  # Ensures user must be logged in
def volunteer_page(request):
    response = helper_verify(request)
    if response:  # Handle unauthorized access
        return response
    name = request.user.first_name

    """
    quantities to be imported:
        1) overall sentiments of reviews made by me (will use half pi chart already made)
        2) Give a description tlaking about their contribution?
    """
    #sentiment extraction 
    reviews = Review.objects.filter(Volunteer=request.user)

    sent_data = {'Very Negative':0, 'Somewhat Negative':0,'Neutral':0,'Somewhat Positive':0,'Very Positive':0}
    for review in reviews: 
        # Analysis data
        sent_data[review.Sentiment] = sent_data.get(review.Sentiment, 0) + 1

    # Convert the sentiment data to a list of dictionaries for easy access
    sentiments_dict = [{'Sentiment': key, 'Occurrences': value} for key, value in sent_data.items()]
    context = {
        'name': name,
        'sentiments_dict': json.dumps(sentiments_dict),
    }
    return render(request, 'volunteers/volunteer_home_page.html',context)

#page that has form for volunteer to submit
@login_required  # Ensures user must be logged in
def volunteer_form(request):
    response = helper_verify(request)
    if response:  # Handle unauthorized access
        return response
    
     # Handle POST request (form submission)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Save the review with additional fields
            review = form.save(commit=False)
            review.Department = form.cleaned_data['Department']
            review.Volunteer = request.user
            review.Volunteer_First_Name = request.user.first_name
            review.Volunteer_Last_Name = request.user.last_name
            review_content = form.cleaned_data['Review_Content']

            
            # Set Up Your HuggingFace API Token
            HUGGINGFACE_API_TOKEN = 'API token'
            os.environ['HUGGINGFACEHUB_API_TOKEN'] = HUGGINGFACE_API_TOKEN

            # Loading a Pre-Trained Model from HuggingFace Hub
            model_name = "cardiffnlp/twitter-roberta-base-sentiment"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name)

            classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

            # Split review into smaller chunks (if necessary)
            chunk_size = 512  # Adjust based on model's token limit
            review_chunks = [review_content[i:i+chunk_size] for i in range(0, len(review_content), chunk_size)]

            # Perform sentiment analysis for each chunk and aggregate results
            results = []
            confidence_scores = []  # To collect the confidence scores for averaging
            for chunk in review_chunks:
                chunk_result = classifier(chunk)  # [{'label': 'LABEL_0', 'score': 0.98}]
                results.extend(chunk_result)
                confidence_scores.extend([result['score'] for result in chunk_result])  # Collecting individual chunk scores

            # Aggregate results: here, we simply take the most frequent sentiment label
            # You can adjust this logic to calculate the average score or use another method
            label_counts = {'LABEL_0': 0, 'LABEL_1': 0, 'LABEL_2': 0}
            for result in results:
                label_counts[result['label']] += 1

            # Determine the overall sentiment label based on most frequent result
            most_frequent_label = max(label_counts, key=label_counts.get)

            # Map sentiment labels to human-readable categories
            sentiment_mapping = {
                "LABEL_0": "Negative",
                "LABEL_1": "Neutral",
                "LABEL_2": "Positive"
            }
            sentiment_label = sentiment_mapping[most_frequent_label]

            # Calculate the average confidence score across all chunks
            average_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0

            # Refine Positive and Negative classes into Very/Somewhat
            if sentiment_label == "Negative":
                if average_confidence > 0.75:
                    review.Sentiment = "Very Negative"
                else:
                    review.Sentiment = "Somewhat Negative"
            elif sentiment_label == "Positive":
                if average_confidence > 0.75:
                    review.Sentiment = "Very Positive"
                else:
                    review.Sentiment = "Somewhat Positive"
            else:  # Neutral
                review.Sentiment = "Neutral"

            # Save the review
            review.save()


            return redirect('volunteer_form')  # Redirect back to the page after submission
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = ReviewForm()  # Create an empty form for GET requests
    context = {
        'form':form,
    }
    return render(request, 'volunteers/volunteer_review_form.html',context)


#volunteer stats
@login_required
def volunteer_stats(request):
    response = helper_verify(request)
    if response:  # Handle unauthorized access
        return response

    """Icons: 
        1) reviews made 
        2) #admin responses available
        3) Average reported rating
        4) Departments Volunteered in

    """
    # Fetch reviews submitted by the current volunteer
    reviews = Review.objects.filter(Volunteer=request.user)
    num_reviews = len(reviews)
    admin_responses = 0
    dep_dict=[]
    num_dep = 0

    rating = 0
    for review in reviews:
        if (review.Admin_Response):
            admin_responses+=1
        if (review.Department not in dep_dict):
            num_dep+=1
            dep_dict.append(review.Department)
        rating+=review.Rating
    #computing average
    rating/=num_reviews
    rating = round(rating, 1) 
    context = {
        'user_reviews': reviews,
        'num_admin_resp': admin_responses,
        'num_dep': num_dep,
        'num_reviews': num_reviews,
        'avg_rating': rating,
        'dep_list': dep_dict,
        'volunteer_info': request.user,
    }

    return render(request, 'volunteers/volunteer_past_reviews.html', context)

#editing/deleting forms is allowed to either admin/volunteer
def verify_admin_vol(request):
    # Check if the logged-in user is a Volunteer
    if not hasattr(request.user, 'role') or (request.user.role != 'volunteer' and request.user.role!='admin'):
        logout(request) #logout
        messages.error(request, "You are not authorized to access this page.")
        login_url = reverse('login')
        return redirect(login_url)  # Redirect to login or another page
    
#editing forms
from .forms import edit_del_form
@login_required
def edit_review(request, id):
    response = verify_admin_vol(request)
    if response:  # Handle unauthorized access
        return response

    review = get_object_or_404(Review, id=id)
    if request.method == 'POST':
        form = edit_del_form(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('volunteer_stats')  # Or any other page you want to redirect to after editing
    else:
        form = edit_del_form(instance=review)

    return render(request, 'volunteers/edit_review.html', {'form': form, 'review': review})

# #deleting review: 
@login_required
def delete_review(request, id):
    response = verify_admin_vol(request)
    if response:  # Handle unauthorized access
        return response

    review = get_object_or_404(Review, id=id)

    if request.method == 'POST':
        review.delete()
        return redirect('volunteer_stats')  # Or any other page you want to redirect to after deleting

    return render(request, 'volunteers/confirm_delete.html', {'review': review})

#for deleting multiple reviews
@csrf_exempt
def delete_reviews(request):
    if request.method == 'POST':
        selected_reviews = request.POST.getlist('selected_reviews')
        if selected_reviews:
            Review.objects.filter(id__in=selected_reviews).delete()
        else:
            messages.error(request, "No reviews selected for deletion.")
    if request.user.role == 'volunteer':
        return redirect('volunteer_stats')
    if request.user.role == 'admin':
        return redirect('admin_review_view')

########################## Admin Pages ##########################
#verify admin
def helper_verify_admin(request):
    # Check if the logged-in user is a Volunteer
    if not hasattr(request.user, 'role') or request.user.role != 'admin':
        logout(request) #logout
        messages.error(request, "You are not authorized to access this page.")
        login_url = reverse('login')
        return redirect(login_url)  # Redirect to login or another page
    

@login_required
def admin_home(request): 
    # Check if the logged-in user is an admin user
    response = helper_verify_admin(request)
    if response:  # Handle unauthorized access
        return response
    """
    items to display: 
        number of reviews for them
        number of departments they have reviews for 
        number of volunteers
    """
    #load in reviews
    review = Review.objects.filter(admin_user = request.user)

    # Initialize counters
    rev_count = 0
    dep_count = 0
    vol_count = 0

    # Using sets to automatically handle uniqueness
    dep_set = set()
    vol_set = set()

    # Loop through the review items
    for item in review:
        #items into sets
        dep_set.add(item.Department)  
        vol_set.add(item.vol_ID)      
        
        rev_count += 1  # Increment review count

    # Extract the counts
    dep_count = len(dep_set)  # The size of the set gives the unique department count
    vol_count = len(vol_set)  # The size of the set gives the unique volunteer count

    # Get the name of the user
    name = request.user.first_name

    # Prepare the context
    context = {
        'name': name,
        'review_count': rev_count,
        'volunteer_count': vol_count,
        'department_count': dep_count,
    }
    return render(request, 'admin_views/admin_home_page.html', context)

#viewing volunteer reviews
@login_required
def admin_review_view(request): 
    # Check if the logged-in user is an admin user
    response = helper_verify_admin(request)
    if response:  # Handle unauthorized access
        return response
    
    """
    Views that we want the admin to have
        1) date submitted
        2) Review content
        3) admin response
        4) user ID
        5) sentiment analysis 
        6) rating 
        7) review content
    """
    # Fetch reviews submitted by the current volunteer
    reviews = Review.objects.filter(admin_user=request.user.username)
    num_reviews = len(reviews)
    admin_responses = 0
    dep_dict=[]
    num_dep = 0

    rating = 0
    for review in reviews:
        if (review.Admin_Response):
            admin_responses+=1
        if (review.Department not in dep_dict):
            num_dep+=1
            dep_dict.append(review.Department)
        rating+=review.Rating
    #computing average
    rating/=num_reviews
    rating = round(rating, 1) 


    name = request.user.first_name
    context = {
        'user_reviews':reviews,
        'name':name,
        'num_admin_resp': (num_reviews-admin_responses),
        'num_dep': num_dep,
        'num_reviews': num_reviews,
        'avg_rating': rating,
        'dep_list': dep_dict,
        'admin_info': request.user,
    }
    return render(request, 'admin_views/admin_vol_reviews.html', context)

#editing admin review
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt  # If you're handling CSRF tokens manually in your JavaScript, you can use this
def update_review(request):
    if request.method == 'POST':
        try:
            # Get the data from the request
            data = json.loads(request.body)
            review_id = data.get('id')
            field = data.get('field')
            value = data.get('value')

            # Fetch the review from the database and update the field
            review = Review.objects.get(id=review_id)
            setattr(review, field, value)
            review.save()

            return JsonResponse({'message': 'Review updated successfully!'}, status=200)

        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

# helper function for the graph function
def normalize_data(department_data, data_points, now):
    """
    Normalize data to exactly 10 data points, filling missing months with zero ratings.
    """
    normalized_data = []
    # Start from the most recent month and go back 10 months
    for i in range(data_points):
        target_date = now - timedelta(days=(i * 30))  # Approximate month interval
        # Find the closest data point within department data for this target date
        closest_data = next((entry for entry in department_data if entry[0].month == target_date.month and entry[0].year == target_date.year), None)
        
        # If no data for this month, append 0
        if closest_data:
            normalized_data.append(closest_data[1])  # Just the average rating for the month
        else:
            normalized_data.append(0)  # No data, append 0
    normalized_data.reverse()
    
    return normalized_data

#analysis view
@login_required
def admin_analysis(request): 
    # Check if the logged-in user is an admin user
    response = helper_verify_admin(request)
    if response:  # Handle unauthorized access
        return response
    
    reviews = Review.objects.filter(admin_user=request.user.username)

    #overall Sentiment of the hospital- separate reviews based on good bad and mediocre on a pie chart
    sent_data = {'Very Negative':0, 'Somewhat Negative':0,'Neutral':0,'Somewhat Positive':0,'Very Positive':0}
    overall_ratings = {i: 0 for i in range(1, 11)}

#-------------------- Previous Reviews -----------------------------
    now = timezone.now()

    # Group by department and month, ensuring 10 months of data
    monthly_averages = (
        Review.objects.annotate(month=TruncMonth('Date_Submitted'))
        .values('month', 'Department')
        .annotate(avg_rating=Avg('Rating'))
        .order_by('Department', 'month')
    )
    
    # Gathering a list of departments
    departments = list(set([entry['Department'] for entry in monthly_averages]))
    
    # Prepare the data in dictionary; each department has an array of ratings per month (10 months)
    data_prev = {'departments': {}}
    
    for department in departments:
        # Collect data for the department: (month, avg_rating)
        department_data = [
            (entry['month'], entry['avg_rating']) for entry in monthly_averages if entry['Department'] == department
        ]
        
        # Normalize the department's data to match the number of data points required (10 months)
        normalized_data = normalize_data(department_data, 10, now)
        
        # Add the normalized data for the department
        data_prev['departments'][department] = normalized_data
        print(data_prev)
#--------------------- Gathering Department  Average Ratings -------------------------------------
    dep_avg_ratings = {}
    dep_rev_count = {}
    dep_sent_count = {}

    # Assuming review has 'Department', 'Rating', and 'Sentiment' as attributes
    for review in reviews:
        department = review.Department
        rating = review.Rating
        sentiment = review.Sentiment  # Assuming the sentiment is directly available in the review

        # Update the total rating sum for the department
        if department in dep_avg_ratings:
            dep_avg_ratings[department] += rating
            dep_rev_count[department] += 1
            # Update sentiment count for the department
            if sentiment in dep_sent_count[department]:
                dep_sent_count[department][sentiment] += 1
            else:
                dep_sent_count[department][sentiment] = 1
        else:
            # Initialize department with first rating, review count, and sentiment count
            dep_avg_ratings[department] = rating
            dep_rev_count[department] = 1
            dep_sent_count[department] = { 'Very Negative': 0, 'Somewhat Negative': 0, 
                                        'Neutral': 0, 'Somewhat Positive': 0, 'Very Positive': 0 }
            dep_sent_count[department][sentiment] = 1  # Initialize sentiment count for the first review

    # Calculate the average for each department
    for department in dep_avg_ratings:
        dep_avg_ratings[department] /= dep_rev_count[department]  # Divide total rating by the count of reviews

#--------------------- Gathering Department Review Numbers -------------------------------------
    dep_rev_num = {} #key: department, value: number of reviews
#---------------------Loop for multiple data selections -------------------------------------
    # Loop to fetch all data
    for review in reviews: 
        # Analysis data
        overall_ratings[review.Rating]+=1
        sent_data[review.Sentiment] = sent_data.get(review.Sentiment, 0) + 1
        dep_rev_num[review.Department] = dep_rev_num.get(review.Department, 0) + 1

    # Convert the sentiment data to a list of dictionaries for easy access
    sentiments_dict = [{'Sentiment': key, 'Occurrences': value} for key, value in sent_data.items()]
    dep_rev_num_dict = [{'Department': key, 'Occurrences': value} for key, value in dep_rev_num.items()]
    overall_ratings_list = [{'Rating': key, 'Occurrences': value} for key, value in overall_ratings.items()]
    dep_avg_rating_v2 = [{'Department': key, 'avg_rating': value} for key, value in dep_avg_ratings.items()]
    # sent_data_dict = [{'Department': key, 'Sentiments': value} for key, value in dep_sent_count.items()]

    # Pass the data as JSON in the context
    context = {
        'sentiments_dict': json.dumps(sentiments_dict),
        'overall_ratings': json.dumps(overall_ratings_list),
        'previous_reviews': json.dumps(data_prev),

        #for horizontal compound plot
        'dep_avg_rating': json.dumps(dep_avg_rating_v2),
        'sent_dep': json.dumps(dep_sent_count),

        #pi chart department review distribution 
        'dep_rev_num':json.dumps(dep_rev_num_dict),
    }

    return render(request, 'admin_views/admin_analysis.html',context)

