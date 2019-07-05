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
    path('word_list_start_contrast', views.word_list_start_contrast, name='word_list_start_contrast'),
    path('refresh_contrast', views.refresh_contrast, name='refresh_contrast'),
    path('experiment', views.experiment_action, name='experiment'),
    path('my_profile', views.my_profile_action, name='my_profile'),
    path('register', views.register_action, name='register'),
    path('confirm-registration/<slug:username>/<slug:token>',
        views.confirm_action, name='confirm'),
    path('forget_password',views.forget,name='forget_password'),
    path('resend_activation',views.resend,name='resend_activation'),
    path('reset_password',views.reset,name='reset_password'),
    path('confirm-reset/<slug:username>/<slug:token>',
        views.confirmreset_action, name='confirmreset'),
]