from django.shortcuts import render, redirect, reverse, get_object_or_404
from boldpredict.forms import RegistrationForm, LoginForm, WordListForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator
from django import forms
from django.http import HttpResponse,Http404

# Used to send mail from within Django
from django.core.mail import send_mail
from django.conf import settings

# stimuli type constant strings
WORD_LIST = "word_list"
IMAGE = "image"
SENTENCE = "sentence"


# Create your views here.
def login_action(request):
    return render(request, 'boldpredict/index.html', {})

@login_required
def logout_action(request):
    logout(request)
    return redirect(reverse('login')) 

def contrast_action(request):
    stimuli_types = settings.STIMULI_TYPES
    model_types = settings.MODEL_TYPES
    context = {}
    context['stimulis'] = stimuli_types
    context['model_types'] = model_types
    return render(request, 'boldpredict/contrast_type.html', context)


def new_contrast(request):
    context = {}
    if request.method != 'GET':
        raise Http404
    if  not request.GET.get('stimuli_type',None) or not request.GET.get('model_type',None):
        context['stimulis'] = settings.STIMULI_TYPES
        context['model_types'] = settings.MODEL_TYPES
        context['error'] = "Please choose both stimuli type and model type!"
        return render(request, 'boldpredict/contrast_type.html', context)

    stimuli_type = request.GET['stimuli_type']
    model_type = request.GET['model_type']
    if stimuli_type == WORD_LIST:
        context['conditions'] = []
        for condition_key,condition_value in settings.WORD_LIST_CONDITIONS.items():
            condition = {}
            condition['name'] = condition_key
            condition['brief_part1'] = condition_value[:30]
            condition['brief_part2'] = condition_value[30:60]
            context['conditions'].append(condition)
        context['form'] = WordListForm()
        return render(request, 'boldpredict/contrast_filler.html', context)
    
    return redirect(reverse('contrast'))
        
def start_contrast(request):
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
    new_user.is_active = False
    new_user.save()
    ##
    #sendverificationmail()
    token = default_token_generator.make_token(new_user)

    email_body = """
    Please click the link below to verify your email address and
    complete the registration of your account:

    http://{host}{path}
    """.format(host=request.get_host(), 
           path=reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="boldpredictionscmu@gmail.com",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'boldpredict/needs-confirmation.html', context)



@transaction.atomic
def confirm_action(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()

    return render(request, 'boldpredict/confirmed.html', {})

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
