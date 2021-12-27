from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name = 'home'),
    path('crud', views.crud, name='crud'),
    path('create', views.RecCreateView.as_view(), name='create'),
    path('visitor', views.RecListView.as_view(), name='visitor'),
    path('<int:pk>/update', views.RecUpdateView.as_view(), name='update'),
    path('new_entry', views.new_entry, name='new_entry'),
    path('<int:pk>/change_entry', views.change_entry, name='change_entry'),
]