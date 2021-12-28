from django.urls import path
from . import views
from libManager import views as lv

urlpatterns = [
    path('', views.index, name = 'index'),
    path('register', views.UserCreateView.as_view(), name = 'register'),
    path('<int:pk>/signup', views.register, name = 'signup'),
    path('login', views.UserLoginView.as_view(), name = 'login'),
    path('signout', views.signout, name = 'signout'),
    path('activate;<uidb64>/<token>', views.activate, name = 'activate'),
    path('libM/home', lv.home, name='home')
]