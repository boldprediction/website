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


@api_view(['GET'])
def experiment_details(request, exp_id):
    experiment = experiment_api.get_experiment(exp_id)
    if experiment is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(experiment.serialize())


@api_view(['DELETE'])
@login_required
def stimuli_details(request, stimuli_id):
    stimuli = Stimuli.objects.get(id=stimuli_id)
    if stimuli is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    stimuli.delete()
    return Response({'id': stimuli_id})


@api_view(['POST','GET'])
@login_required
def contrast_list(request, exp_id):
    """ 
    List all snippets, or create a new snippet.
    """
    exp = Experiment.objects.get(id=exp_id)
    if request.method == 'POST':
        contrasts = request.data
        contrast_ids = []
        for contrast in contrasts:
            contrast_title = contrast["contrast_name"]
            condition1 = contrast['condition1']
            condition2 = contrast['condition2']
            privacy_choice = contrast['privacy_choice']
            baseline_choice = contrast['baseline_choice']
            permutation_choice = contrast['permutation_choice']

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
            contrast = Contrast.objects.create(contrast_title=contrast_title, baseline_choice=baseline_choice,
                                               permutation_choice=permutation_choice, experiment=exp,
                                               privacy_choice=privacy_choice, creator=request.user,
                                               hash_key=hash_key,figure_list = json.dumps(figures))

            condition1['contrast_id'] = contrast.id
            condition2['contrast_id'] = contrast.id
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
                    Coordinate.objects.create(coordinate_name=coordinate_name,
                                            x=x, y=y, z=z, zscore=zscore, contrast=contrast)

            contrast_ids.append(contrast.id)
        return Response({'contrast_ids': contrast_ids})
    elif request.method == 'GET':
        contrasts_result = []
        for contrast in exp.contrasts:
            contrast_dict = {}
            contrast_dict['contrast_name'] = contrast.contrast_title
            contrast_dict['privacy_choice'] = privacy_choice
            contrast_dict['baseline_choice'] = baseline_choice
            contrast_dict['permutation_choice'] = permutation_choice
            contrast['figures'] = json.loads(figures_list)
            condition1_dict,condition2_dict = {}, {}
            condition1,condition2 = contrast.conditions[0], contrast.conditions[1] 
            condition1_dict['name'] = condition1.condition_name
            stimuli_list1 = [ stimuli.id for stimuli in condition1.stimulus]
            condition1_dict['stimuli_list'] = stimuli_list1
            contrast['condition1'] = condition1_dict
            
            condition2_dict['name'] = condition2.condition_name
            stimuli_list2 = [ stimuli.id for stimuli in condition2.stimulus]
            condition2_dict['stimuli_list'] = stimuli_list2
            contrast['condition2'] = condition2_dict

            coordinates = []
            for coordinate in contrast.coordinates:
                coordinate_dict = {}
                coordinate_dict['zscore'] = coordinate.zscore
                coordinate_dict['x'] = coordinate.x
                coordinate_dict['y'] = coordinate.y
                coordinate_dict['z'] = coordinate.z
                coordinate_dict['name'] = coordinate.coordinate_name
                coordinates.append(coordinate_dict)
            contrast['coordinates'] = coordinates

        return Response(contrasts_result)


def get_text(condition):
    text = []
    for stimuli_key in condition['stimuli_list']:
        stimuli = Stimuli.objects.get(id=stimuli_key)
        stimuli_dict = stimuli.serializer()
        text.append(stimuli_dict['stimuli_content'])
    return ','.join(text)
