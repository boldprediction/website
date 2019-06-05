from django.shortcuts import render, redirect, reverse, get_object_or_404
from boldpredict.forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout



# Create your views here.
def login_action(request):
    pass 

def logout_action(request):
    logout(request)
    return redirect(reverse('login')) 

def contrast_action(request):
    pass 

def index(request):
    pass 

def experiment_action(request):
    pass 


def my_profile_action(request):
    pass 

def register_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'boldpredict/register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'boldpredict/register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])

    new_user.save()
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request, new_user)
    return redirect(reverse('index'))
