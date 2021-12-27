from django.urls import path, include
from . import views
from libManager import views as lv

urlpatterns = [
    path('', views.index, name = 'index'),
    path('register', views.register, name = 'register'),
    path('login', views.login, name = 'login'),
    path('signout', views.signout, name = 'signout'),
    path('activate;<uidb64>/<token>', views.activate, name = 'activate'),
    path('libM/home', lv.home, name='home')
]