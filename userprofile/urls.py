from django.urls import path,include
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('',views.profile,name="profile"),
    path('editprofile',views.editprofile,name='editprofile')
    
]