from urllib.request import urlopen

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
from django.http import HttpResponse, Http404, HttpResponseBadRequest

# Used to send mail from within Django
from django.core.mail import send_mail
from django.conf import settings
import json
from boldpredict.models import *
from boldpredict.api import contrast_api, sqs_api, cache_api, experiment_api, stimuli_api

# constants
from boldpredict import constants
from datetime import datetime

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import base64


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


def not_implement(request):
    return render(request, 'boldpredict/not_implemented.html', {})


def word_list_contrast(request, model_type):
    context = {}
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
    context['stimuli_type'] = constants.WORD_LIST
    return render(request, 'boldpredict/word_list_contrast_filler.html', context)


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
    page_name = constants.CONTRAST_FILLER.get(stimuli_type, None)
    if page_name is None:
        return redirect(reverse('not_implement'))
    return redirect(reverse(page_name, kwargs={'model_type': model_type}))


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

    c_id, find, hash_key = contrast_api.check_existing_contrast(**params)
    if find:
        return redirect(reverse('contrast_results_view', kwargs={'contrast_id': c_id}))

    params['hash_key'] = hash_key
    contrast = contrast_api.create_word_list_contrast(**params)
    sqs_api.send_contrast_message(sqs_api.create_contrast_message(
        contrast), stimuli_type)

    context['contrast_id'] = contrast.id
    context['host_ip'] = settings.HOST_IP
    context['app_port'] = settings.APPLICATION_PORT
    context['timeout_interval'] = settings.TIMEOUT_INTERVAL
    context['refresh_interval'] = settings.REFRESH_INTERVAL
    return render(request, 'boldpredict/processing.html', context)


def index(request):
    return render(request, 'boldpredict/index.html', {})


def experiment_action(request):
    # published_exps = Experiment.objects.filter(is_published = True ).filter( is_approved = True )
    published_exps = Experiment.objects.filter(
        is_published=True).filter(status=constants.APPROVED)
    txt = ''
    template = '<br> <h4> <li> <a  href={0}> {1} </a> </li> </h4> <br> '
    for exp in published_exps:
        txt += template.format('/experiment/{0}'.format(exp.id),
                               exp.experiment_title)
    return render(request, 'boldpredict/experiment_list.html', {'txt': txt})


def experiment_detail(request, exp_id):
    exp = Experiment.objects.get(pk=exp_id)
    template = '<br> <h4>  <li> <a target="_parent" href={0}> {1} </a> </li> </h4> '
    txt = ''
    contrasts = exp.contrasts.all()
    for contrast in contrasts:
        txt += template.format('/contrast_results/{0}'.format(
            contrast.id), contrast.contrast_title)
    return render(request, 'boldpredict/experiment.html', {'title': exp.experiment_title,
                                                           'DOI': exp.DOI, 'authors': exp.authors,
                                                           'txt': txt})


@login_required
def experiment_edit(request, exp_id):
    exp = Experiment.objects.get(pk=exp_id)
    if not (exp.is_published and (exp.creator.username == request.user.username or request.user.is_superuser)):
        raise Http404
    stimuli_types = constants.STIMULI_TYPES
    model_types = constants.MODEL_TYPES
    coordinate_types = constants.COORDINATE_TYPES
    context = {}
    context['stimulis'] = stimuli_types
    context['model_types'] = model_types
    context['coordinate_types'] = coordinate_types
    context['settings'] = {
        'coordinate_space': exp.coordinate_space,
        'stimuli_type': exp.stimuli_type,
        'model_type': exp.model_type
    }
    context['experiment_title'] = exp.experiment_title
    context['authors'] = exp.authors
    context['DOI'] = exp.DOI
    context['exp_id'] = exp_id
    return render(request, 'boldpredict/new_experiment.html', context)


@login_required
def new_experiment(request):
    stimuli_types = constants.STIMULI_TYPES
    model_types = constants.MODEL_TYPES
    coordinate_types = constants.COORDINATE_TYPES
    context = {}
    context['stimulis'] = stimuli_types
    context['model_types'] = model_types
    context['coordinate_types'] = coordinate_types
    context['settings'] = {
        'coordinate_space': MNI,
        'stimuli_type': WORD_LIST,
        'model_type': ENG1000
    }
    return render(request, 'boldpredict/new_experiment.html', context)


@login_required
def save_stimuli(request):
    return render(request, 'boldpredict/index.html', {})


# remove and replace with edit contrasts instead
@login_required
def add_contrast(request):
    return render(request, 'boldpredict/add_contrast.html')


@login_required
def edit_contrasts(request, exp_id):
    exp = Experiment.objects.get(pk=exp_id)
    if not (exp.is_published and (exp.creator.username == request.user.username or request.user.is_superuser)):
        raise Http404
    stimuli_type = exp.stimuli_type
    return render(request, 'boldpredict/add_contrast.html', {'exp_id': exp_id})


@login_required
def upload_images(request):
    if request.method == 'POST':
        experiment_id = request.POST['experiment_id']
        res = []
        for k, v in request.FILES.items():
            # get index information, front end needs this information back
            parts = k.split("@")
            if len(parts) < 3:
                continue
            i, j = parts[0], parts[1]
            filename = '@'.join(parts[2:])

            # get the real file name
            parts = filename.split(".")
            if len(parts) < 2:
                continue

            # add extra information like experiment and time onto the file name
            name = '.'.join(parts[:-1]) + "@" + str(experiment_id) + "@" + datetime.now().strftime(
                '%Y-%m-%dT%H-%M-%S') + '.' + parts[-1]

            # store the to-be-returned information
            res.append({"i": i, "j": j, "name": name})

            # write file onto the disk
            with open(settings.UPLOAD_IMAGE_ROOT + name, 'wb+') as destination:
                for chunk in v.chunks():
                    destination.write(chunk)

    return HttpResponse(json.dumps(res))


@login_required
def save_experiment(request):
    if request.method != 'POST':
        raise Http404

    stimuli_types = constants.STIMULI_TYPES
    model_types = constants.MODEL_TYPES
    coordinate_types = constants.COORDINATE_TYPES
    error_context = {}
    error_context['stimulis'] = stimuli_types
    error_context['model_types'] = model_types
    error_context['coordinate_types'] = coordinate_types
    error_context['settings'] = {
        'coordinate_space': request.POST.get('coordinate_space', MNI),
        'stimuli_type': request.POST.get('stimuli_type', WORD_LIST),
        'model_type': request.POST.get('model_type', ENG1000)
    }
    error_context['experiment_title'] = request.POST.get(
        'experiment_title', "")
    error_context['authors'] = request.POST.get('authors', "")
    error_context['DOI'] = request.POST.get('DOI', "")

    if 'experiment_title' not in request.POST or not len(request.POST['experiment_title']):
        error_context['error'] = "Please input experiment title"
        return render(request, 'boldpredict/new_experiment.html', error_context)

    if 'authors' not in request.POST or not len(request.POST['authors']):
        error_context['error'] = "Please input authors"
        return render(request, 'boldpredict/new_experiment.html', error_context)

    if 'DOI' not in request.POST or not len(request.POST['DOI']):
        error_context['error'] = "Please input DOI"
        return render(request, 'boldpredict/new_experiment.html', error_context)

    if 'coordinate_space' not in request.POST:
        error_context['error'] = "Please choose a coordinate space"
        return render(request, 'boldpredict/new_experiment.html', error_context)

    if 'stimuli_type' not in request.POST:
        error_context['error'] = "Please choose a type of stimulus"
        return render(request, 'boldpredict/new_experiment.html', error_context)

    if 'model_type' not in request.POST:
        error_context['error'] = "Please choose a model type"
        return render(request, 'boldpredict/new_experiment.html', error_context)

    params = request.POST.dict()
    params['is_published'] = True

    stimuli_type = request.POST['stimuli_type']
    stimuli_page = constants.EXPERIMENT_STIMULI_FILLER.get(stimuli_type, None)
    if stimuli_page is None:
        return redirect(reverse('not_implement'))

    if 'exp_id' in request.POST and len(request.POST['exp_id']) > 0:
        # save new content
        params['exp_id'] = request.POST['exp_id']
        exp = experiment_api.update_experiment(**params)
        return redirect(reverse(stimuli_page, args=(int(request.POST['exp_id']),)))
    
    if request.user.is_authenticated:
        params['creator'] = request.user
    exp = experiment_api.create_experiment(**params)
    return redirect(reverse(stimuli_page, args=(int(exp.id),)))


@login_required
def word_edit_stimuli(request, exp_id):
    exp = Experiment.objects.get(pk=exp_id)
    if not (exp.is_published and (exp.creator.username == request.user.username or request.user.is_superuser)):
        raise Http404
    stimuli_type = exp.stimuli_type
    return render(request, 'boldpredict/word_add_stimuli.html', {'exp_id': exp_id, 'stimuli_type': stimuli_type})


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


@login_required
def my_profile_experiment_list(request):
    exps = Experiment.objects.filter(
        is_published=True).filter(creator__username=request.user.username)
    experiments = [exp.serialize() for exp in exps.all()]
    context = {"experiments": experiments}
    return render(request, "boldpredict/my_profile_experiment_list.html", context)


@login_required
def my_profile_contrast_list(request):
    contrasts = Contrast.objects.filter(
        experiment__is_published=False).filter(creator__username=request.user.username)
    contrast_list = [con.serialize() for con in contrasts.all()]
    context = {"contrasts": contrast_list}
    return render(request, "boldpredict/my_profile_contrast_list.html", context)


@login_required
def my_profile_approval_list(request):
    if not request.user.is_superuser:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    exps = Experiment.objects.filter(
        is_published=True).filter(status=constants.SUBMITTED)
    experiments = [exp.serialize() for exp in exps.all()]
    context = {"experiments": experiments}
    return render(request, 'boldpredict/my_profile_approval_list.html', context)


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


def get_contrast(request):
    if not request.GET.get('contrast_id', None):
        raise Http404
    contrast_id = request.GET['contrast_id']
    contrast = contrast_api.get_contrast_dict_by_id(contrast_id)
    if contrast is None:
        raise Http404
    return HttpResponse(json.dumps(contrast), content_type='application/json')


def subj_result_view(request, subj_name, contrast_id):
    context = {}
    subj_str = contrast_api.get_contrast_subj_webgl_strs(
        contrast_id, subj_name)
    context['subject_url'] = settings.SUBJECTS_URL
    context['subject_cstr'] = subj_str
    context['subject_name'] = subj_name
    context['subject_json_file'] = subj_name + constants.SUBJECT_JSON_SUFFIX
    return render(request, 'boldpredict/subject.html', context)


def contrast_results_view(request, contrast_id):
    contrast = contrast_api.get_contrast_dict_by_id(contrast_id)
    contrast['subject_num'] = settings.SUBJECT_NUM
    for i in range(8):
        subject_key = "subject" + str(i + 1)
        if i < settings.SUBJECT_NUM:
            subject_name = settings.SUBJECTS[i]
            contrast[subject_key] = subject_name
        else:
            contrast[subject_key] = "dummy"

    if contrast and contrast['stimuli_type'] == WORD_LIST:
        contrast['image_url'] = settings.IMAGE_URL
        return render(request, 'boldpredict/word_list_contrast_results.html', contrast)
    return redirect(reverse('not_implement'))


@csrf_exempt
def update_contrast(request):
    if request.method != 'POST':
        raise Http404

    contrasts_results = json.loads(request.body)
    print("contrasts_results = ", contrasts_results)
    response_data = {}
    response_data['contrast_ids'] = []
    for contrast_result in contrasts_results:
        contrast_id = contrast_result['contrast_info']['id']
        group_analyses = contrast_result['group_analyses']
        subjects_analyses = contrast_result['subjects_analyses']
        try:
            print("contrast_id - ", contrast_id, " group_analyses = ", group_analyses, "subjects_analyses = ",
                  subjects_analyses)
            contrast_api.update_contrast_result(
                contrast_id, group_analyses, subjects_analyses)
            response_data['contrast_ids'].append(contrast_id)
        except:
            raise HttpResponseBadRequest

    return HttpResponse(json.dumps(response_data), content_type='application/json')


@csrf_exempt
def create_contrast(request):
    if request.method != 'POST':
        raise Http404

    params = json.loads(request.body)

    c_id, find, hash_key = contrast_api.check_existing_contrast(**params)
    if find:
        return HttpResponse(json.dumps({'contrast_id': c_id, 'hash_key': str(hash_key)}),
                            content_type='application/json')

    params['hash_key'] = hash_key
    contrast = contrast_api.create_contrast(**params)
    sqs_api.send_contrast_message(sqs_api.create_contrast_message(
        contrast), params['stimuli_type'])

    return HttpResponse(json.dumps({'contrast_id': str(contrast.id), 'hash_key': str(contrast.hash_key)}),
                        content_type='application/json')
