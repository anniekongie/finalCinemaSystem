from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
import string,random


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User,AbstractUser

from .models import UserInfo
from .forms import loginForm, registerForm, EditProfileForm
from booking.models import Order
from movies.models import MovieInfo
from datetime import datetime
# Create your views here.

def home(request):
    movieObj=MovieInfo.objects.all()
    return render(request, 'home.html', {'movies': movieObj})

def login(request):
    username='not logged in'
    if request.method=='POST':
        LoginInfo=loginForm(request.POST)
        if LoginInfo.is_valid():
            username=LoginInfo.cleaned_data['email']
    else:
        LoginInfo=loginForm()
    
    return render(request, 'home.html')

def signUp(request):
    user=None;
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            email = form.clean_email()
            firstname = form.getFirstName()
            lastname = form.getLastName()
            user=form.save()
            #sending the email
            current_site=get_current_site(request)
            mail_subject='Activate your account.'
            message=render_to_string('activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email=form.cleaned_data.get('email')
            email=EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            #return redirect('http://127.0.0.1:8000/accounts/activation/')
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            user = registerForm()
    return render(request, 'registration/register.html', {'form': user})

def activate(request, uidb64, token):
    User=get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def editProfile(request):
    if request.method=='POST':
        form = EditProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
        else:
            return HttpResponse(form.errors)
    else:
        form=EditProfileForm(instance=request.user)
        context={
            'form':form
            }
        return render(request, 'editProfile.html', context)

def viewProfile(request):
    
    context={
        'user':request.user
        }
    return render(request,'profile.html',context)

def changePassword(request):
    if request.method=='POST':
        form=PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('http://127.0.0.1:8000/accounts/profile/')
        else:
            return HttpResponse(form.errors)
    else:
        form=PasswordChangeForm(user=request.user)
        context={'form':form}
        return render(request,'change_password.html',context)

def orderHistory(request,userid):
    user=UserInfo.objects.get(id2=userid)
    history=Order.objects.filter(userAccount=user).filter(isPaid=True)
    currtime=datetime.now()
    context={
        'history':history,
        'currtime':currtime
        }
    return render(request,'orderHistory.html',context)
