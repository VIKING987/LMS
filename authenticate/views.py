from django.shortcuts import redirect, render
from . models import User
from . forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import CreateView, UpdateView, ListView, FormView
from django.contrib.auth.hashers import make_password
from . tokens import generateToken
from LMS import settings


# Create your views here.
def index(request):
    return render(request, 'authenticate/index.html')


class UserCreateView(CreateView):
    model = User
    form_class = RegisterForm

    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        return super().form_valid(form)

def register(request, pk):

    ruser = User.objects.get(id=pk)
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

class UserLoginView(FormView):
    fields = '__all__'
    form_class = LoginForm
    template_name = 'authenticate/login.html'
    success_url = 'libM/home'

    def form_valid(self, form):
        form_data = form.cleaned_data
        user = authenticate(username = form_data['username'], password = form_data['password'])
        if user is not None:
            auth_login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Invalid Credentials!!")
            return redirect('login')


def signout(request):
    if request.user.is_anonymous:
        pass
    else:
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
        messages.success(request, 'Account Activated! Login To Continue!!')
        return redirect('login')
    else:
        return render(request, 'authenticate/activation_failed.html')