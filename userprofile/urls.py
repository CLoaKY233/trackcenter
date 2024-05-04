from django.urls import path,include
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('/editprofile',views.editprofile,name='editprofile'),
    path('',views.profile,name="profile"),
]