import datetime
import time
import boto3
from django.conf import settings
from boldpredict.constants import *
import json

auto_client = boto3.client('autoscaling')
sqs_client = boto3.client('sqs')


def send_contrast_message(message, stimuli_type):
    response = sqs_client.send_message(
        QueueUrl=settings.QUERY_URL,
        MessageBody = json.dumps(message),
        DelaySeconds=1,
        MessageAttributes={
            'StimuliType': {
                'StringValue': stimuli_type,
                'DataType': 'String'
            }
        }
    )

def create_contrast_sqs_word_list_message(contrast):
    message_body = {}
    stimulus_dict = {}
    stimulus = contrast.experiment.stimulus.all()
    for stimuli in stimulus:
        stimuli_dict = {}
        word_list_stimuli = stimuli.word_list_stimuli
        stimuli_dict['type'] = WORD_LIST
        stimuli_dict['value'] = word_list_stimuli.word_list
        stimulus_dict[stimuli.stimuli_name] = stimuli_dict
    message_body['stimuli'] = stimulus_dict

    contrast_dict = {} 
    conditions_dict = {}
    conditions_dict['figures'] = []
    conditions_dict['coordinates'] = []
    conditions = contrast.conditions.all()
    for i in range(len(conditions)):
        condition = conditions[i]
        condition_list = [ stimuli.stimuli_name for stimuli in condition.stimulus.all()]
        condition_name_str = 'condition' + str(i+1)
        conditions_dict[condition_name_str] = condition_list
    conditions_dict['contrast_id'] = str(contrast.id)

    contrast_dict['contrast1'] = conditions_dict
    message_body['contrasts'] = contrast_dict
    message_body['do_perm']  = contrast.permutation_choice
    message_body['coordinate_space'] = contrast.experiment.coordinate_space
    message_body['DOI'] = contrast.experiment.DOI
    message_body['model_type'] = contrast.experiment.model_type
    return message_body


def create_contrast_sqs_message(contrast):
    stimuli_type  = contrast.experiment.stimuli_type
    if stimuli_type == WORD_LIST:
        return create_contrast_sqs_word_list_message(contrast)
    else:
        return {}

