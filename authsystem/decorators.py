from django.http import HttpResponse
from django.shortcuts import redirect,render
from .models import permissionmanager



def teachercheck(view_func):
    def wrapper_func(request,*args,**kwargs):
        userperms=permissionmanager.objects.get(user=request.user)
        if userperms.is_teacher:
            return view_func(request ,*args,**kwargs)
        else :
            return redirect("homepage")
    return wrapper_func




def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return view_func(request,*args,**kwargs)
        else:
            return redirect('signin')
            
    return wrapper_func

def authenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('homepage')
            
        else:
            return view_func(request,*args,**kwargs)
            
    return wrapper_func