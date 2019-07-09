from django.contrib import admin
from boldpredict.models import *

admin.site.register([Experiment, Contrast, Stimuli,WordListStimuli,Condition,Coordinate])

# from django.contrib.auth import User
# Register your models here.
# admin.site.register(User)