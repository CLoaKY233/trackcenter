from django.urls import path,include
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('',views.tableview,name='tableview')
]