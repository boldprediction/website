import datetime
import time
import boto3
from django.conf import settings
from boldpredict.constants import *
import json

sqs_client = boto3.client('sqs', region_name=settings.REGION_NAME, aws_access_key_id=settings.AWS_ACCESS_KEY,
                   aws_secret_access_key=settings.AWS_SECRET_KEY)


def send_contrast_message(message, stimuli_type):
    response = sqs_client.send_message(
        QueueUrl=settings.SQS_QUERY_URL,
        MessageBody = json.dumps(message),
        DelaySeconds=1,
        MessageAttributes={
            'StimuliType': {
                'StringValue': stimuli_type,
                'DataType': 'String'
            }
        }
    )

def create_word_list_contrast_message(contrast):
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

    contrasts_dict = {} 

    contrast_params_dict = {}
    contrast_params_dict['figures'] = []
    contrast_params_dict['coordinates'] = []
    conditions = contrast.conditions.all()
    for i in range(len(conditions)):
        condition = conditions[i]
        condition_list = [ stimuli.stimuli_name for stimuli in condition.stimulus.all()]
        condition_name_str = 'condition' + str(i+1)
        contrast_params_dict[condition_name_str] = condition_list
    contrast_params_dict['do_perm']  = contrast.permutation_choice
    contrast_params_dict['num_perm']  = 1000 if contrast.permutation_choice else 0
    
    contrasts_dict[str(contrast.id)] = contrast_params_dict
    message_body['contrasts'] = contrasts_dict
    message_body['coordinate_space'] = contrast.experiment.coordinate_space
    message_body['DOI'] = contrast.experiment.DOI
    message_body['semantic_model'] = contrast.experiment.model_type
    return message_body


def create_contrast_message(contrast):
    stimuli_type  = contrast.experiment.stimuli_type
    if stimuli_type == WORD_LIST:
        return create_word_list_contrast_message(contrast)
    else:
        return {}


