from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('new_contrast', views.new_contrast, name='new_contrast'),
    path('refresh_contrast', views.refresh_contrast, name='refresh_contrast')
]