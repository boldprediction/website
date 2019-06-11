from django.shortcuts import render, redirect, reverse, get_object_or_404
from boldpredict.forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

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
