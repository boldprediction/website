from django.shortcuts import render, redirect, reverse, get_object_or_404
from boldpredict.forms import RegistrationForm, LoginForm, ForgotForm, ResetForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction,models
from django.http import Http404
# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator
from django import forms

# Used to send mail from within Django
from django.core.mail import send_mail

from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def login_action(request):
    return render(request, 'boldpredict/index.html', {})

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
    if request.method != 'GET':
        return Http404
    user = request.user
    context = {}
    context['username'] = user.username
    context['first_name'] = user.first_name
    context['last_name'] = user.last_name
    context['email'] = user.email
    
    return render(request, 'boldpredict/my_profile.html', context)


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

    if new_user is not None:
        login(request, new_user)
        return redirect(reverse('index'))
    else:
        return redirect(reverse('login'))

#reset password
# note : There is an inherit flaw in this logic.
def reset(request):
    context = {}
    form = ResetForm(request.POST)
    context['form'] = form
    context['username'] = request.POST['username']
    if not form.is_valid():
        return render(request, 'boldpredict/reset_password.html', context)

    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            user.set_password(request.POST['password'])
            user.save()
            messages.success(request, "Your password has been changed.")
            return redirect(reverse('login'))
        except ObjectDoesNotExist:
            return render(request, 'boldpredict/forget_password.html', {})



#This is to reset the password
# This is hit through the email's link 
@transaction.atomic
def confirmreset_action(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, route the user to reset password page.
    reset_context = {}
    reset_form = ResetForm()
    reset_context['form'] = reset_form
    reset_context['username'] = username

    return render(request, 'boldpredict/reset_password.html', reset_context)


#forgot password function which triggers the mail 
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
        user = User.objects.get(email=form.cleaned_data['email'])
        print(user.email)

        token = default_token_generator.make_token(user)
        email_body = """
        Please click the link below to change the password of your BoldPredictions account:
        http://{host}{path}
        """.format(host=request.get_host(),path=reverse('confirmreset', args=(user.username, token)))

        send_mail(subject="Verify your email address",message= email_body,from_email="boldpredictionscmu@gmail.com",recipient_list=[user.email])
        context['email'] = form.cleaned_data['email']
        return render(request, 'boldpredict/needs-confirmation1.html', context)

    except ObjectDoesNotExist:
        context['messages'] = messages
        messages.append("email id does not exist in our database")
        return render(request, 'boldpredict/forget_password.html', context)

############---------------forgot_initial_implementation------------------#############
#Initial implementation of forget function which resets the password without a mail link 
#forgot password function which triggers the mail 
# def forget(request):
#     context = {}
    
    
#     if request.method == 'GET':
#         context['form'] = ForgotForm()
#         return render(request, 'boldpredict/forget_password.html', context)

#     form = ForgotForm(request.POST)
#     if not form.is_valid():
#         return render(request, 'boldpredict/forget_password.html', context)

#     reset_context = {}
#     reset_form = ResetForm()
#     messages = []
#     try:
#         user = User.objects.get(username=form.cleaned_data['username'])
#         if (user.email == form.cleaned_data['email']):
#             u1= User.objects.get(email=form.cleaned_data['email'])
#             print(u1.email)
#             reset_context['form'] = reset_form
#             reset_context['username'] = form.cleaned_data['username']
#             return render(request, 'boldpredict/reset_password.html', reset_context)
#         else:
#             messages.append("Username does not match email address")
#             context['messages'] = messages
#             return render(request, 'boldpredict/forget_password.html', context)
#     except ObjectDoesNotExist:
#         context['messages'] = messages
#         messages.append("User does not exist with username")
#         return render(request, 'boldpredict/forget_password.html', context)
############-------------------------------------------------------#############


