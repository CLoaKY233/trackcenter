from django.shortcuts import render
from django.contrib.auth.models import User
from .models import userprofile
from authsystem.decorators import *
from django.contrib import messages
# Create your views here.


@unauthenticated_user
def profile(request):
    user = request.user
    info = userprofile.objects.get(user=user)
    user_profile = {
        'username': user.username,
        'regno':info.user_regno,
        'fname': user.first_name,
        'lname': user.last_name,
        'github_id': info.user_githubid,
        'project_name': info.project_name,
        'project_link': info.project_link,
        'project_about': info.project_about,
        'email_address': user.email,

    }
    

    # Pass the dictionary data as context to the template
    return render(request, 'userprofile/profile.html', {'user_profile': user_profile})

@unauthenticated_user
def editprofile(request):
    if request.method == "POST":
        user = request.user
        info = userprofile.objects.get(user=user)
        
        
        if request.POST['email'] == '':  # Check if the email field is empty
            user.email = user.email
        else:# If it is, set the email to the current email
            email = request.POST['email']
            if User.objects.filter(email=email):
                messages.error(request, "Email already registered, please retry with another email")
                return render(request,'userprofile/editprofile.html',{'messages': messages.get_messages(request)})  
            user.email = email
            
            
        if request.POST['github_id'] == '':  # Check if the email field is empty
            info.user_githubid=info.user_githubid
        else:# If it is, set the email to the current email
            githubid = request.POST['github_id']
            if userprofile.objects.filter(user_githubid=githubid):
                messages.warning(request, "github link already registered, please recheck")
                return render(request,'userprofile/editprofile.html',{'messages': messages.get_messages(request)})  
            info.user_githubid = githubid

        
        info.project_name = request.POST['project_name'] if request.POST['project_name'] else info.project_name
        info.project_link = request.POST['project_link'] if request.POST['project_link'] else info.project_link
        info.project_about = request.POST['project_about'] if request.POST['project_about'] else info.project_about
        user.save()
        info.save()
        messages.success(request, 'Profile updated successfully') 
        return redirect('profile')
        # Add a success message
    else:
        messages.success(request, 'Hello there!, profile changes here will reflect immidietly! Please proceed with caution')  # Add an error message for GET requests
    
    return render(request, 'userprofile/editprofile.html', {'messages': messages.get_messages(request)})