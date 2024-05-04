from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def profile(request):
    user = request.user
    user_profile = {
        'username': user.username,
        'fname': user.first_name,
        'lname': user.last_name,
        'github_id': '1990-01-01',
        'project_name': 'https://github.com/john_doe',
        'project_link': 'Sample Project',
        'project_about': 'https://github.com/john_doe/sample_project',
        'email_address': 'Sample Project',

    }

    # Pass the dictionary data as context to the template
    return render(request, 'userprofile/profile.html', {'user_profile': user_profile})


def editprofile(request):
    pass
