from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from authsystem.models import permissionmanager
from django.contrib import messages
from userprofile.models import userprofile
from .models import projectgrade



# Create your views here.



#decorator for teachers only!
def tableview(request):
    users = User.objects.filter(permissionmanager__is_active=True,permissionmanager__is_student=True,permissionmanager__is_teacher=False)
    return render(request, 'reviewer/tableview.html', {'users': users})

def search(request):
    if request.method == 'POST':
        search = request.POST.get('query')
        users = User.objects.filter(permissionmanager__is_active=True, permissionmanager__is_student=True, permissionmanager__is_teacher=False, userprofile__user_regno__icontains=search)
        messages.success(request, f'Search results for {search}')
        return render(request, 'reviewer/tableview.html', {'users': users, 'messages': messages.get_messages(request)})
    messages.warning(request, 'An error occoured!')
    return redirect("tableview")

#decorator for teachers only!
def gradeview(request):
    if request.method == 'POST':
        regno= request.POST.get('student')
        totalmarks = int(request.POST.get('marks'))
        remarks = request.POST.get('remarks')
        print(remarks,totalmarks)
        user = User.objects.get(userprofile__user_regno=regno)
        if user is None:
            messages.error(request, 'User not found!')
            return redirect('tableview')
        
        userperms=permissionmanager.objects.get(user=user)
        if userperms.is_teacher:
            messages.error(request, 'User is a teacher!')
            return redirect('tableview')
        if userperms.is_active is False:
            messages.error(request, 'User is not verified!')
            return redirect('tableview')
        
        
        
        usergrade=projectgrade.objects.get(user=user)
        usergrade.grade = (totalmarks)
        usergrade.remarks = remarks
        usergrade.is_graded = True
        
        usergrade.save()
        messages.success(request, f'Graded {user.first_name} {user.last_name} with {totalmarks} and remarks: {remarks}')
        return redirect('tableview')
    return render(request, 'reviewer/tableview.html',{'messages':messages.get_messages(request)})

#decorator for students only!
def remarksview(request):
    pass