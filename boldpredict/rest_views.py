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
import boldpredict.utils as utils

# constants
from boldpredict import constants

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import base64


@api_view(['POST'])
@login_required
def stimuli_list(request):
    """ 
    List all snippets, or create a new snippet.
    """
    if request.method == 'POST':
        request_data = request.data
        if 'stimuli_name' in request_data and 'stimuli_type' in request_data   \
                and 'stimuli_content' in request_data and 'exp_id' in request_data:
            stimuli = stimuli_api.create_stimuli(**request_data)
            return Response(stimuli.serialize(), status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def experiment_details(request, exp_id):
    experiment = experiment_api.get_experiment(exp_id)
    if experiment is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(experiment.serialize())
    elif request.method == 'POST':
        data = request.data
        data['exp_id'] = exp_id
        experiment_api.update_experiment(**data)
        experiment = experiment_api.get_experiment(exp_id)
        return Response(experiment.serialize())
    elif request.method == 'DELETE':
        experiment.delete()


@api_view(['DELETE'])
def contrast_details(request, c_id):
    contrast = Contrast.objects.get(id=c_id)
    contrast.delete()
    return Response({'id': c_id})


@api_view(['DELETE'])
@login_required
def stimuli_details(request, stimuli_id):
    stimuli = Stimuli.objects.get(id=stimuli_id)
    if stimuli is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    stimuli.delete()
    return Response({'id': stimuli_id})


@api_view(['GET'])
def stimulus_list(request, exp_id):
    experiment = experiment_api.get_experiment(exp_id)
    if experiment is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        exp_dict = experiment.serialize()
        return Response(exp_dict['stimuli'])


@api_view(['POST', 'GET'])
@login_required
def contrast_list(request, exp_id):
    """ 
    List all snippets, or create a new snippet.
    """
    exp = Experiment.objects.get(id=exp_id)
    if request.method == 'POST':
        contrasts = request.data
        contrast_ids = []
#       delete previous contrasts
        for contrast in exp.contrasts.all():
            contrast_api.delete_contrast(contrast.id)

        for contrast in contrasts:
            contrast_title = contrast["contrast_name"]
            condition1 = contrast['condition1']
            condition2 = contrast['condition2']
            privacy_choice = contrast.get('privacy_choice', PUBLIC)
            baseline_choice = contrast.get('baseline_choice', False)
            permutation_choice = contrast.get('permutation_choice', False)

            params = {}
            params['stimuli_type'] = exp.stimuli_type
            params['model_type'] = exp.model_type
            params['coordinate_space'] = exp.coordinate_space
            params['owner'] = request.user
            params['list1_text'] = get_text(condition1)
            params['list2_text'] = get_text(condition2)
            params['contrast_type'] = privacy_choice

            hash_key = utils.generate_hash_key(**params)
            figures = contrast['figures'] if "figures" in contrast else []
            contrast_obj = Contrast.objects.create(contrast_title=contrast_title, baseline_choice=baseline_choice,
                                                   permutation_choice=permutation_choice, experiment=exp,
                                                   privacy_choice=privacy_choice, creator=request.user,
                                                   hash_key=hash_key, figures_list=json.dumps(figures))

            condition1['contrast_id'] = contrast_obj.id
            condition2['contrast_id'] = contrast_obj.id
            contrast_api.create_condition(**condition1)
            contrast_api.create_condition(**condition2)

            if "coordinates" in contrast:
                coordinates = contrast['coordinates']
                for coordinate in coordinates:
                    coordinate_name = coordinate['name']
                    x = coordinate['x']
                    y = coordinate['y']
                    z = coordinate['z']
                    zscore = coordinate['zscore']
                    tscore = coordinate.get('tscore', 0)
                    voxel = coordinate.get('voxel', 0)
                    Coordinate.objects.create(coordinate_name=coordinate_name,
                                              x=x, y=y, z=z, zscore=zscore,
                                              tscore=tscore, voxel=voxel,
                                              contrast=contrast_obj)

            contrast_ids.append(str(contrast_obj.id))
            sqs_api.send_contrast_message(sqs_api.create_contrast_message(
                contrast_obj), exp.stimuli_type)
        return Response({'contrast_ids': contrast_ids})

    elif request.method == 'GET':
        contrasts_result = []
        for contrast in exp.contrasts.all():
            contrast_dict = {}
            contrast_dict['id'] = str(contrast.id)
            contrast_dict['contrast_name'] = contrast.contrast_title
            contrast_dict['privacy_choice'] = contrast.privacy_choice
            contrast_dict['baseline_choice'] = contrast.baseline_choice
            contrast_dict['permutation_choice'] = contrast.permutation_choice
            contrast_dict['figures'] = json.loads(contrast.figures_list)
            condition1_dict, condition2_dict = {}, {}
            contrast_conditions = contrast.conditions.all()
            if len(contrast_conditions) >= 1:
                condition1 = contrast_conditions[0]
                condition1_dict['name'] = condition1.condition_name
                stimuli_list1 = [
                    stimuli.id for stimuli in condition1.stimulus.all()]
                condition1_dict['stimuli_list'] = stimuli_list1
                contrast_dict['condition1'] = condition1_dict
            if len(contrast_conditions) >= 2:
                condition2 = contrast_conditions[1]
                condition2_dict['name'] = condition2.condition_name
                stimuli_list2 = [
                    stimuli.id for stimuli in condition2.stimulus.all()]
                condition2_dict['stimuli_list'] = stimuli_list2
                contrast_dict['condition2'] = condition2_dict
            coordinates = []
            for coordinate in contrast.coordinates.all():
                coordinate_dict = {}
                coordinate_dict['voxel'] = coordinate.voxel
                coordinate_dict['tscore'] = coordinate.tscore
                coordinate_dict['zscore'] = coordinate.zscore
                coordinate_dict['x'] = coordinate.x
                coordinate_dict['y'] = coordinate.y
                coordinate_dict['z'] = coordinate.z
                coordinate_dict['name'] = coordinate.coordinate_name
                coordinates.append(coordinate_dict)
            contrast_dict['coordinates'] = coordinates
            contrasts_result.append(contrast_dict)

        return Response(contrasts_result)


def get_text(condition):
    text = []
    for stimuli_key in condition['stimuli_list']:
        stimuli = Stimuli.objects.get(id=stimuli_key)
        stimuli_dict = stimuli.serialize()
        text.append(stimuli_dict['stimuli_content'])
    return ','.join(text)


@api_view(['GET'])
@login_required
def user_contrast_list(request, username):
    if request.user.username != username:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    contrasts = Contrast.objects.filter(experiment__is_published = False).filter(creator__username=username)
    contrast_list = [con.serialize() for con in contrasts.all()]
    return Response(contrast_list)


@api_view(['POST'])
@login_required
def experiment_email(request, exp_id):
    exp = Experiment.objects.get(id=exp_id)
    administrators = User.objects.filter(is_superuser=True)
    email_addresses = [u.email for u in administrators.all()]
    email_body = """
    Please click the link below to edit and approve the submitted published experiment:
    http://{host}{path}
    """.format(host=request.get_host(),
               path=reverse('experiment_edit', args=(exp_id, )))
    send_mail(subject="Approve published experiment" + exp.experiment_title,
              message=email_body,
              from_email="boldpredictionscmu@gmail.com",
              recipient_list=email_addresses)

    return Response({"exp_id": exp_id})


@api_view(['POST'])
@login_required
def experiment_approval(request, exp_id):
    if request.user.is_superuser == False:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    data = {}
    data['exp_id'] = exp_id
    # data['is_approved'] = True
    data['status'] = constants.APPROVED
    experiment_api.update_experiment(**data)
    exp = experiment_api.get_experiment(exp_id)
    return Response(exp.serialize())


@api_view(['POST'])
@login_required
def experiment_reject(request, exp_id):
    if request.user.is_superuser == False:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    data = {}
    data['exp_id'] = exp_id
    # data['is_approved'] = True
    data['status'] = constants.REJECT
    experiment_api.update_experiment(**data)
    exp = experiment_api.get_experiment(exp_id)
    return Response(exp.serialize())


@api_view(['GET'])
@login_required
def experiment_list(request, username):
    if request.user.username != username:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    exps = Experiment.objects.filter(
        is_published=True).filter(creator__username=username)
    experiments = [exp.serialize() for exp in exps.all()]
    return Response(experiments)
