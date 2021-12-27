from django.shortcuts import redirect, render
from . models import User
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from libManager import views
from . tokens import generateToken
import re
from LMS import settings


# Create your views here.

def checkreqpass(password):
    f = [0,0,0]
    for ch in password:
        if ch.islower():
            f[0] = 1
        if ch.isupper():
            f[1] = 1
        if ch.isnumeric():
            f[2] = 1
    
    if f[0]==0 or f[1]==0 or f[2]==0:
        return 0
    
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if(regex.search(password) == None):
        return 0

    return 1


def index(request):
    return render(request, 'authenticate/index.html', {})

def register(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        designation = request.POST.get('designation')

        if User.objects.filter(username = username):
            messages.error(request, "Username Already In Use!!")

            return redirect('register')

        if User.objects.filter(email = email):
            messages.error(request, "Email Already In Use!!")

            return redirect('register')

        if len(username)>10:
            messages.error(request, "Username Can't Be Greater Than 10 Characters")

            return redirect('register')

        if len(pass1)<6:
            messages.error(request, "Password Can't Be Less Than 6 Characters")

            return redirect('register')

        if len(pass1)>20:
            messages.error(request, "Password Can't Be Greater Than 20 Characters")

            return redirect('register')

        if not checkreqpass(pass1):
            messages.error(request, "Passwords Requirements Not Fulfilled!! Must contain: 0-9/A-Z/a-z and special character(s)")

            return redirect('register')

        if pass1 != pass2:
            messages.error(request, "Passwords Do Not Match!!")

            return redirect('register')

        if designation is None:
            messages.error(request, "You Have Not Selected Between Librarian And Visitor!!")

            return redirect('register')

        ruser = User.objects.create_user(username, email, pass1)
        ruser.fname = fname
        ruser.lname = lname
        ruser.is_active = False
        ruser.designation = designation
        ruser.save()

        messages.success(request, "Your Account Has Been Successfully Created!! Please Confirm Your Email")

        current_site = get_current_site(request)
        subject = "Welcome To The City Library!"
        message = render_to_string('authenticate/confirmation.html', {
            'name' : ruser.fname,
            'domain' : current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(ruser.pk)),
            'token' : generateToken.make_token(ruser)
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [ruser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('login')

    return render(request, 'authenticate/register.html')

def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username = username, password = pass1)

        if user is not None:
            auth_login(request, user)
            #return render(request, home, {'fname' : fname})
            return redirect('libM/home')
        
        else:
            messages.error(request, "Wrong Password or Username")
            return redirect('index')

    return render(request, 'authenticate/login.html', {})

def signout(request):
    logout(request)
    messages.success(request, "You Have Been Successfully Logged Out!!")
    return redirect('index')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        ruser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        ruser = None
    
    if ruser is not None and generateToken.check_token(ruser, token):
        ruser.is_active = True
        ruser.save()
        auth_login(request, ruser)
        #return render(request, 'libM/home', {'fname' : ruser.first_name})
        return redirect('libM/home')
    else:
        return render(request, 'authenticate/activation_failed.html')