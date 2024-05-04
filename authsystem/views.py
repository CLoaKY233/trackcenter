from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from.models import permissionmanager
from .decorators import teachercheck,unauthenticated_user,authenticated_user
from django.http import HttpResponse

from userprofile.models import userprofile


def index(request):
    if request.user.is_authenticated:
        fname = request.user.first_name
        return render(request, 'authsystem/index.html',{'fname':fname})
    else:
        return render(request, 'authsystem/index.html')

@authenticated_user
def signup(request):
    if request.method == 'POST':
        username= request.POST['username']
        email = request.POST['email']
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2= request.POST['pass2']
        
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists, please chose another one")
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered, please login!")
            return redirect('signin')
        if len(username) > 12:
            messages.error(request, "Username must be under 12 characters")
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric")
            return redirect('signup')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

    
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        
        userperms=permissionmanager(user=myuser)
        userperms.save()
        
        userprofileinfo = userprofile(user=myuser)
        userprofileinfo.save()
        
        
        
        messages.success(request, "Your account has been successfully created")
        return redirect('signin')
    return render(request, 'authsystem/signup.html')

@authenticated_user
def signin(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "Successfully logged in")
            return render(request,'authsystem/index.html',{'fname':fname})
        else:
            messages.error(request, "Invalid credentials, please try again")
            return redirect('signin')
    return render(request, 'authsystem/signin.html')











def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('homepage')

