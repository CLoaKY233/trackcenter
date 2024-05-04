from django.urls import path,include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('signup', views.signup, name='signup'),
    #path('signup/', RedirectView.as_view(url='/signup')),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    
    
    

#    path('changepassword',views.changepassword,name='changepassword'),
#    path('resetpassword',views.resetpassword,name='resetpassword'),

    
    
    
    
    
    
    
#    path('markupdater', views.markupdater,name='markupdater'),
    
    
    
    
]