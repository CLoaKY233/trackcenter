from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from.models import permissionmanager
from .decorators import teachercheck,unauthenticated_user,authenticated_user
from django.http import HttpResponse
from django.core.mail import send_mail,EmailMultiAlternatives
from userprofile.models import userprofile
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.html import strip_tags
from reviewer.models import projectgrade

import openpyxl





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
            messages.warning(request, "Username already exists, please chose another one")
            return redirect('signup')
        
        
        
        if User.objects.filter(email=email):
            user=User.objects.get(email=email)
            userperms=permissionmanager.objects.get(user=user)
            if userperms.is_active==True:
                messages.warning(request, "Email already registered!, please sign in")
                return redirect('signin')
            elif userperms.is_active==False:
                messages.warning(request, "Similar Email was found, please activate your account asap")
                

        
        
        
        
        # if User.objects.filter(email=email):
        #     messages.warning(request, "Email already registered, please login!")
        #     return redirect('signin')
        if len(username) > 12:
            messages.warning(request, "Username must be under 12 characters")
        if not username.isalnum():
            messages.warning(request, "Username must be alphanumeric")
            return redirect('signup')
        if pass1 != pass2:
            messages.warning(request, "Passwords do not match")
            return redirect('signup')

    
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        
        userperms=permissionmanager(user=myuser)
        userperms.is_active = False
        userperms.activation_key = default_token_generator.make_token(myuser)
        userperms.save()
        
        userprofileinfo = userprofile(user=myuser)
        userprofileinfo.save()
        
        grade=projectgrade(user=myuser)
        grade.save()
        
        send_activation_email(request, myuser)

        send_mail(
            subject='Account Created!',
            message=f'Hello {firstname + lastname}\nYour account has been successfully created on Trackcenter\n',
            from_email='exhibitionease.auth@gmail.com',
            recipient_list=[f'{email}'],
            fail_silently=True,  # Set to True if you don't want to raise exceptions
        )        
        messages.success(request, "Your account has been successfully created")
        return redirect('signin')
    return render(request, 'authsystem/signup.html')


# def send_activation_email(request, user):
#     current_site = get_current_site(request)
#     subject = 'Activate your account'
#     activation_key = default_token_generator.make_token(user)
#     message = render_to_string('authsystem/activation_email.html', {
#         'user': user,
#         'domain': current_site.domain,
#         'activation_key': activation_key,
#     })
#     user.email_user(subject, message=message)


def send_activation_email(request, user):
    current_site = get_current_site(request)
    subject = 'Activate your account'
    activation_key = default_token_generator.make_token(user)
    context = {
        'user': user,
        'domain': current_site.domain,
        'activation_key': activation_key,
    }
    
    # Render both HTML and plain text versions of the email content
    html_message = render_to_string('authsystem/activation_email.html', context)
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email='exhibitionease.auth@gmail.com',
        to=[user.email]
    )
    email.attach_alternative(html_message, "text/html")

    email.send()


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
            messages.warning(request, "Invalid credentials, please try again")
            return redirect('signin')
    return render(request, 'authsystem/signin.html')











def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('homepage')






def activate_account(request, activation_key):


    if not request.user.is_authenticated:
        messages.warning(request, "You need to be logged in to activate your account")
        return redirect('signin')

    try:
        user = request.user
        userperms = permissionmanager.objects.get(user=user)
        userkey = userperms.activation_key
        userinfo = userprofile.objects.get(user=user)
        if activation_key == userkey:
            
            workbook=openpyxl.load_workbook('authsystem\data.xlsx')
            sheet = workbook.active
            
                
            for row in sheet.iter_rows(values_only=True):
                if row[2] == user.email:
                    # User email exists in the sheet
                    regno = row[0]
                    name = row[1]
                    break
            else:
                # User email does not exist in the sheet
                messages.warning(request, "You are not allowed to activate this account. Please contact the admin.")
                return redirect('homepage')
            
            
            name = name.split()
            user.first_name = name[0]
            user.last_name=name[-1]
            
            userinfo.user_regno=regno
            
            userperms.is_active=True
            # # Send email notification to user
            # send_mail(
            #     subject='Account Activated',
            #     message=f'Your account has been activated.\n Registeration Number -> {regno}\nName : {name} \nEmail : {user.email}',
            #     from_email='exhibitionease.auth@gmail.com',
            #     recipient_list=[user.email],
            #     fail_silently=False
            # )


            userinfo.save()
            user.save()
            userperms.save()
            messages.success(request, "Your account has been activated")
            redirect('homepage')
        else:
            messages.warning(request, "Invalid activation key")

    except (TypeError, ValueError, OverflowError, User.DoesNotExist, permissionmanager.DoesNotExist) as e:
        messages.warning(request, f"Failed to activate your account: {e}")
    return redirect('homepage')