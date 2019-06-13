from django.shortcuts import render
from archpoc.models import *
from django.http import HttpResponse



# Create your views here.

def index(request):
    return render(request, 'archpoc/index.html', {})

def new_contrast(request):
    new_contrast = Contrast()
    new_contrast.save()
    print("new_contrastid = ", new_contrast.id)
    return render(request, 'archpoc/wait_contrast.html', {'contrast_id': new_contrast.id})

def refresh_contrast(request):
    contrast_id = request.GET['contrast_id']
    contrast = Contrast.objects.get(id=contrast_id)
    json_msg = ""
    # contrast.image_location = "" #dummy
    if contrast.image_location:
        json_msg = '{ "image_location": "'+contrast.image_location+ \
                   '", "success": "true" }'
    else:
        json_msg = '{ "success": "false" }'
    return HttpResponse(json_msg, content_type='application/json')

def receive_result(request):
    contrast_id = request.POST['contrast_id']
    image_location = request.POST['image_location']
    contrast = Contrast.objects.get(id=contrast_id)
    contrast.image_location = image_location
    json_msg = '{ "success": "false" }'
    return HttpResponse(json_msg, content_type='application/json')
