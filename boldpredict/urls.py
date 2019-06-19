from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.index, name='index'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('contrast', views.contrast_action, name='contrast'),
    path('new_contrast', views.new_contrast, name='new_contrast'),
    path('start_contrast', views.start_contrast, name='start_contrast'),
    path('experiment', views.experiment_action, name='experiment'),
    path('my_profile', views.my_profile_action, name='my_profile'),
    path('register', views.register_action, name='register'),
    path('confirm-registration/<slug:username>/<slug:token>',
        views.confirm_action, name='confirm'),
]