from django.shortcuts import render
from django.contrib.auth.models import User
from .models import userprofile
# Create your views here.
def profile(request):
    user = request.user
    info = userprofile.objects.get(user=user)
    user_profile = {
        'username': user.username,
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


def editprofile(request):
    pass
