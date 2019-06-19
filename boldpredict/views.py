from django.shortcuts import render, redirect, reverse, get_object_or_404
from boldpredict.forms import RegistrationForm, LoginForm, ForgotForm, ResetForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.
# def login_action(request):
#     return render(request, 'boldpredict/index.html', {})

@login_required
def logout_action(request):
    logout(request)
    return redirect(reverse('login')) 

def contrast_action(request):
    return render(request, 'boldpredict/index.html', {})

def index(request):
    return render(request, 'boldpredict/index.html', {})
 

def experiment_action(request):
    return render(request, 'boldpredict/index.html', {}) 

@login_required
def my_profile_action(request):
    return render(request, 'boldpredict/index.html', {})


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
    return redirect(reverse('login'))

#Login Action
def login_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'boldpredict/login.html', context)

    form = LoginForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'boldpredict/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('index'))
    # if new_user is not None:
    #     return redirect(reverse('register'))
    #     login(request, new_user)
    # else:
    #     messages.error(request,'Username or Password is incorrect')
    #     return redirect(reverse('login'))

#reset password
def reset(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            user.set_password(request.POST['password'])
            print("Password changed")
            user.save()
            return redirect(reverse('login'))
        except ObjectDoesNotExist:
            return render(request, 'boldpredict/forget_password.html', {})

def forget(request):
    context = {}
    
    
    if request.method == 'GET':
        context['form'] = ForgotForm()
        return render(request, 'boldpredict/forget_password.html', context)

    form = ForgotForm(request.POST)
    if not form.is_valid():
        return render(request, 'boldpredict/forget_password.html', context)

    reset_context = {}
    reset_form = ResetForm()
    messages = []
    try:
        user = User.objects.get(username=form.cleaned_data['username'])
        if (user.email == form.cleaned_data['email']):
            reset_context['form'] = reset_form
            reset_context['username'] = form.cleaned_data['username']
            return render(request, 'boldpredict/reset_password.html', reset_context)
        else:
            messages.append("Username does not match email address")
            context['messages'] = messages
            return render(request, 'boldpredict/forget_password.html', context)
    except ObjectDoesNotExist:
        context['messages'] = messages
        messages.append("User does not exist with username")
        return render(request, 'boldpredict/forget_password.html', context)

