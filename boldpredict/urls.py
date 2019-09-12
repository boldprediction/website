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
    path('experiment', views.experiment_action, name='experiment'),
    path('experiment/<int:exp_id>', views.experiment_detail, name='experiment_detail'),
    path('new_experiment', views.new_experiment, name='new_experiment'),
    path('my_profile', views.my_profile_action, name='my_profile'),
    path('register', views.register_action, name='register'),
    path('confirm-registration/<slug:username>/<slug:token>',
        views.confirm_action, name='confirm'),
    path('forget_password',views.forget,name='forget_password'),
    path('resend_activation',views.resend,name='resend_activation'),
    path('reset_password',views.reset,name='reset_password'),
    path('confirm-reset/<slug:username>/<slug:token>',
        views.confirmreset_action, name='confirmreset'),
    path('api/update_contrast', views.update_contrast, name='update_contrast'),
    path('api/create_contrast', views.create_contrast, name='create_contrast'),
    path('api/get_contrast', views.get_contrast, name='get_contrast'),
    path('contrast_results/<slug:subj_name>/<slug:contrast_id>', views.subj_result_view, name='subj_result_view'),
    path('contrast_results/<slug:contrast_id>', views.contrast_results_view, name='contrast_results_view'),
]