from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from authsystem.models import permissionmanager
from django.contrib import messages
from userprofile.models import userprofile



# Create your views here.



#decorator for teachers only!
def tableview(request):
    
    
    users = User.objects.filter(permissionmanager__is_active=True,permissionmanager__is_student=True,permissionmanager__is_teacher=False)
    return render(request, 'reviewer/tableview.html', {'users': users})

def search(request):
    if request.method == 'GET':
        search = request.GET['query']
        users = User.objects.filter(permissionmanager__is_active=True,permissionmanager__is_student=True,permissionmanager__is_teacher=False,userprofile__user_regno__icontains=search)
        return render(request, 'reviewer/tableview.html', {'users': users})
    return HttpResponse("hehe")

#decorator for teachers only!
def checker(request):
    pass

#decorator for teachers only!
def gradeview(request):
    pass

#decorator for students only!
def remarksview(request):
    pass