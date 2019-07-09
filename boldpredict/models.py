from django.db import models
from hashid_field import HashidAutoField
from boldpredict.constants import *

class Experiment(models.Model):
    title = models.TextField('experiment_title')
    authors = models.TextField('authors_name',null=True)
    DOI = models.TextField('DOI',null=True)
    
    stimili_type = models.CharField('Stimuli Type',choices=STIMULI_TYPE_CHOICE, max_length=20,default=WORD_LIST) 
    coordinates_space = models.CharField('Coordinate Space',choices=COORDINATE_SPACE_CHOICE, max_length=20,default=MNI) 
    model_type = models.CharField('Model Type',choices=MODEL_TYPE_CHOICE, max_length=20,default=ENG1000) 
    # contrasts_res = models.TextField('model str')
    # objects = ExpManager()

class Stimuli(models.Model):
    name = models.TextField('name of stimuli',max_length=200)
    stimili_type = models.CharField('Stimuli Type',choices=STIMULI_TYPE_CHOICE, max_length=20,default=WORD_LIST) 
    experiment = models.ForeignKey(Experiment,related_name="stimulus",on_delete=models.CASCADE)

class WordListStimuli(models.Model):
    word_list = models.TextField(max_length=10000)
    parent_stimuli = models.OneToOneField(Stimuli, related_name='word_list_stimuli',on_delete=models.CASCADE)

# Create your models here.
class Contrast(models.Model):
    id = HashidAutoField(primary_key=True)
    privacy_choice = models.CharField('Contrast Privacy Settings',choices=PRIVACY_CHOICES, max_length=2,default=PUBLIC) 
    contrast_title = models.TextField('Contrast Title (Optional)', blank=True)
    baseline_choice = models.BooleanField('Compare to baseline', default=False)
    permutation_choice = models.BooleanField('Run permutation/bootstrap test(needs more waiting time)', default=False)
    experiment = models.ForeignKey(Experiment,related_name="contrasts",on_delete=models.CASCADE)
    MNIstr = models.TextField('MNI res str')
    subjstr = models.TextField('subject res str')
    
    # experiment_id = models.BigIntegerField('experiment if it exists',default=0)
    # figures_list = models.TextField('Enter name of Condition 1', default = '')
    # pmaps = models.TextField('permutation parameter')
    # replicated_figure = models.TextField('replicated_image',  default = '')
    # random_roi_file = models.TextField('random_roi_file',  default = '')
    # list1_name = models.TextField('Enter name of Condition 1')
    # list1_text = models.TextField('Enter stimulus words separated by a comma')
    # list2_name = models.TextField('Enter name of Condition 2')
    # list2_text = models.TextField ('Enter stimulus words separated by a comma')

# class Coordinates_holder(models.Model):
#     title = models.TextField('', default = '')
#     roi_image_filename = models.TextField('',  default = '')
#     allmasks = models.TextField('',  default = '')
#     contrast = models.ForeignKey(Contrast,on_delete=models.CASCADE)

class Condition(models.Model):
    name = models.TextField('Condition name',max_length=200)
    stimulus = models.ManyToManyField(Stimuli,related_name='related_conditions')
    contrast  = models.ForeignKey(Contrast,related_name="conditions",on_delete=models.CASCADE)

class Coordinates(models.Model):
    name = models.TextField('roi name')
    x = models.IntegerField('x')
    y = models.IntegerField('y')
    z = models.IntegerField('z')
    contrast = models.ForeignKey(Contrast,on_delete=models.CASCADE)
    # coordinates_holder = models.ForeignKey(Coordinates_holder)

# class Figures(models.Model):
    
# class Author(models.Model):
#     first_name = models.CharField(max_length=20)
#     last_name = models.CharField(max_length=20)

