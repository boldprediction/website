from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, reverse, get_object_or_404
from boldpredict.forms import RegistrationForm, LoginForm, ForgotForm, ResetForm, WordListForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.http import Http404
# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator
from django import forms
from django.http import HttpResponse, Http404

# Used to send mail from within Django
from django.core.mail import send_mail
from django.conf import settings
import json
from boldpredict.models import *
from boldpredict.api import contrast_api, sqs_api

# constants
from boldpredict import constants

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def login_action(request):
    return render(request, 'boldpredict/index.html', {})


@login_required
def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


def contrast_action(request):
    stimuli_types = constants.STIMULI_TYPES
    model_types = constants.MODEL_TYPES
    context = {}
    context['stimulis'] = stimuli_types
    context['model_types'] = model_types
    return render(request, 'boldpredict/contrast_type.html', context)


def new_contrast(request):
    context = {}
    if request.method != 'GET':
        raise Http404
    if not request.GET.get('stimuli_type', None) or not request.GET.get('model_type', None):
        context['stimulis'] = constants.STIMULI_TYPES
        context['model_types'] = constants.MODEL_TYPES
        context['error'] = "Please choose both stimuli type and model type!"
        return render(request, 'boldpredict/contrast_type.html', context)

    stimuli_type = request.GET['stimuli_type']
    model_type = request.GET['model_type']
    if stimuli_type == constants.WORD_LIST:
        context['word_list_suggestions'] = json.dumps(
            constants.WORD_LIST_CONDITIONS)
        context['conditions'] = []
        for condition_key, condition_value in constants.WORD_LIST_CONDITIONS.items():
            condition = {}
            condition['name'] = condition_key
            condition['brief_part1'] = condition_value[:25]
            condition['brief_part2'] = condition_value[25:50]
            context['conditions'].append(condition)
        context['form'] = WordListForm()
        context['public'] = True
        context['model_type'] = model_type
        context['stimuli_type'] = stimuli_type
        return render(request, 'boldpredict/word_list_contrast_filler.html', context)

    return redirect(reverse('contrast'))


def word_list_start_contrast(request):
    context = {}
    if request.method != 'POST':
        raise Http404

    form = WordListForm(request.POST)
    contrast_type = request.POST['contrast_type']
    model_type = request.POST['model_type']
    stimuli_type = request.POST['stimuli_type']

    if contrast_type == 'Private':
        context['public'] = False
    else:
        context['public'] = True

    context['form'] = form

    if not form.is_valid():
        context['model_type'] = model_type
        context['stimili_type'] = stimuli_type
        context['word_list_suggestions'] = json.dumps(
            constants.WORD_LIST_CONDITIONS)
        context['conditions'] = []
        for condition_key, condition_value in constants.WORD_LIST_CONDITIONS.items():
            condition = {}
            condition['name'] = condition_key
            condition['brief_part1'] = condition_value[:25]
            condition['brief_part2'] = condition_value[25:50]
            context['conditions'].append(condition)
        return render(request, 'boldpredict/contrast_filler.html', context)

    params = request.POST.dict()
    params['baseline_choice'] = form.clean_baseline_choice()
    params['permutation_choice'] = form.clean_permutation_choice()
    if request.user.is_authenticated:
        params['owner'] = request.user
    contrast = contrast_api.create_single_word_list_contrast(**params)
    sqs_api.send_contrast_message(sqs_api.create_contrast_message(
        contrast), stimuli_type)

    context['contrast_id'] = contrast.id
    context['host_ip'] = settings.HOST_IP
    context['app_port'] = settings.APPLICATION_PORT
    return render(request, 'boldpredict/processing.html', context)


def index(request):
    return render(request, 'boldpredict/index.html', {})


def experiment_action(request):
    # return render(request, 'boldpredict/MNI_Test.html', {})
    return render(request, 'boldpredict/index.html', {})


@login_required
def my_profile_action(request):
    if request.method != 'GET':
        raise Http404
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
    # sendverificationmail()
    token = default_token_generator.make_token(new_user)

    email_body = """
    Please click the link below to verify your email address and
    complete the registration of your account:

    http://{host}{path}
    """.format(host=request.get_host(),
               path=reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message=email_body,
              from_email="boldpredictionscmu@gmail.com",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'boldpredict/needs_confirmation.html', context)


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

# Login Action


def login_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'boldpredict/login.html', context)

    form = LoginForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'boldpredict/login.html', context)

    try:
        users = User.objects.get(username=form.cleaned_data['username'])
        if not users.is_active:
            context['email'] = users.email
            return render(request, 'boldpredict/resend_activation.html', context)

    except ObjectDoesNotExist:
        return render(request, 'boldpredict/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('index'))

# reset password


def resend(request):
    try:
        user = User.objects.get(email=request.POST['email'])
        if user.is_active:
            return redirect(reverse('login'))

        token = default_token_generator.make_token(user)
        email_body = """
        Please click the link below to verify your email address and
        complete the registration of your account:
        
        http://{host}{path}
        """.format(host=request.get_host(), path=reverse('confirm', args=(user.username, token)))

        send_mail(subject="Verify your email address",
                  message=email_body,
                  from_email="boldpredictionscmu@gmail.com",
                  recipient_list=[user.email])

        form = LoginForm(request.POST)
        context = {}
        context['email'] = request.POST['email']
        return render(request, 'boldpredict/needs_confirmation.html', context)

    except ObjectDoesNotExist:
        messages.error("account not found")
        return redirect(reverse('login'))

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


# This is to reset the password
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


# forgot password function which triggers the mail
def forget(request):
    context = {}
    context['form'] = ForgotForm()
    if request.method == 'GET':
        return render(request, 'boldpredict/forget_password.html', context)

    form = ForgotForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'boldpredict/forget_password.html', context)

    # reset_context = {}
    # reset_form = ResetForm()
    try:
        user = User.objects.get(email=form.cleaned_data['email'])

        token = default_token_generator.make_token(user)
        email_body = """
        Please click the link below to change the password of your BoldPredictions account:
        http://{host}{path}
        """.format(host=request.get_host(), path=reverse('confirmreset', args=(user.username, token)))

        send_mail(subject="Verify your email address", message=email_body,
                  from_email="boldpredictionscmu@gmail.com", recipient_list=[user.email])
        context['email'] = form.cleaned_data['email']
        return render(request, 'boldpredict/static_resetpassword.html', context)

    except ObjectDoesNotExist:
        forgot_context = {}
        forgot_context['form'] = ForgotForm()
        return render(request, 'boldpredict/forget_password.html', forgot_context)


def refresh_contrast(request):
    if not request.GET.get('contrast_id', None):
        raise Http404
    contrast_id = request.GET['contrast_id']
    contrast = contrast_api.get_contrast_dict(contrast_id)
    if contrast is None:
        raise Http404
    if not contrast['result_generated']:
        json_msg = '{ "success": "false" }'
    else:
        json_msg = '{ "success": "true" }'
    return HttpResponse(json_msg, content_type='application/json')

def subj_result_view(request, subj_name, contrast_id):
    context = {}
    subj_str = contrast_api.get_contrast_subj_webgl_strs(contrast_id, subj_name)
    context['subject_url'] = settings.SUBJECTS_URL
    context['subject_cstr'] = subj_str
    context['subject_name'] = subj_name
    context['subject_json_file'] = settings.SUBJECTS_JSON.get(subj_name,'')
    return render(request, 'boldpredict/subject.html', context)

def contrast_results_view(request, contrast_id):
    contrast = contrast_api.get_contrast_dict(contrast_id)
    contrast['subject_num'] = settings.SUBJECT_NUM
    for i in range(8):
        subject_key = "subject" + str(i+1)
        if i < settings.SUBJECT_NUM:
            subject_name = settings.SUBJECTS[i]
            contrast[subject_key] = subject_name
        else:
            contrast[subject_key] = "dummy"

    if contrast and contrast['stimuli_type'] == WORD_LIST:
        return render(request, 'boldpredict/word_list_contrast_results.html', contrast)
    return render(request, 'boldpredict/index.html', {})

def __get_response_json_dict(data={}, err_code=0, message="Success"):
    ret = {
        'err_code': err_code,
        'message': message,
        'data': data
    }
    return ret

@csrf_exempt
def update_contrast(request):
    if request.method != 'POST':
        JsonResponse(__get_response_json_dict(
            err_code=403, message="Forbidden Request"))

    contrasts_results = json.loads(request.body)
    response_data = {}
    response_data['contrast_ids'] = []
    for contrast_result in contrasts_results:
        contrast_id = contrast_result['contrast_info']['id']
        group_analyses = contrast_result['group_analyses']
        subjects_analyses = contrast_result['subjects_analyses']
        try:
            contrast_api.update_contrast_result(contrast_id, group_analyses, subjects_analyses)
            response_data['contrast_ids'].append(contrast_id)
        except:
            JsonResponse(__get_response_json_dict( err_code=400, message="Bad Request"))
    
    return JsonResponse(__get_response_json_dict(data=response_data))
