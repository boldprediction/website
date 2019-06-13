from django.shortcuts import render
from boldpredict.models import *
from django.http import HttpResponse
import boto3




# Create your views here.

def send_message(contrast_id):
    sqs = boto3.client('sqs', region_name='us-east-2', aws_access_key_id='AKIAJBP54APIS46KJMUA',
    aws_secret_access_key='YrgasZ5S23GlO3RwwpZYZrEGsMDKBvRLiWJAjEMA')

    #queue_url = 'https://sqs.us-east-2.amazonaws.com/591395577019/BoldPredictions	'
    queue_url = 'https://sqs.us-east-2.amazonaws.com/280175692519/bold_sqs'
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'ContrastID': {
                'DataType': 'Number',
                'StringValue': str(contrast_id)
            }
        },
        MessageBody=(
            'Request to process contrastID ' + str(contrast_id)
        )
    )


def index(request):
    return render(request, 'boldpredict/index.html', {})

def new_contrast(request):
    new_contrast = Contrast()
    new_contrast.save()
    send_message(new_contrast.id)
    print("new_contrastid = ", new_contrast.id)
    return render(request, 'boldpredict/wait_contrast.html', {'contrast_id': new_contrast.id})

def refresh_contrast(request):
    contrast_id = request.GET['contrast_id']
    contrast = Contrast.objects.get(id=contrast_id)
    json_msg = ""
    # contrast.image_location = "" #dummy
    print("refersh contrast image location = ",contrast.image_location )
    if contrast.image_location:
        json_msg = '{ "image_location": "'+contrast.image_location+ \
                   '", "success": "true" }'
    else:
        json_msg = '{ "success": "false" }'
    return HttpResponse(json_msg, content_type='application/json')

def receive_result(request):
    contrast_id = request.GET['contrast_id']
    image_location = request.GET['image_location']
    contrast = Contrast.objects.get(id=contrast_id)
    contrast.image_location = image_location
    contrast.save()
    print("contrast image location = ",contrast.image_location )
    json_msg = '{ "success": "true" }'
    return HttpResponse(json_msg, content_type='application/json')
