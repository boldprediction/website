from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('', views.login_action, name='login_action'),
    # path('login', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
]