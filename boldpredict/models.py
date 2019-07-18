from django.contrib.auth.models import User
from django.db import models
from hashid_field import HashidAutoField
from boldpredict.constants import *


class Experiment(models.Model):
    experiment_title = models.TextField(
        'experiment_title', null=True, blank=True)
    authors = models.TextField('authors_name', null=True, blank=True)
    DOI = models.TextField('DOI', null=True, blank=True)
    creator = models.ForeignKey(
        User, related_name='has_experiments', on_delete=models.CASCADE, null=True)
    stimuli_type = models.CharField(
        'Stimuli Type', choices=STIMULI_TYPE_CHOICE, max_length=20, default=WORD_LIST)

    coordinate_space = models.CharField(
        'Coordinate Space', choices=COORDINATE_SPACE_CHOICE, max_length=20, default=MNI)

    model_type = models.CharField(
        'Model Type', choices=MODEL_TYPE_CHOICE, max_length=20, default=ENG1000)


class Stimuli(models.Model):
    stimuli_name = models.TextField('name of stimuli', max_length=50)
    stimuli_type = models.CharField(
        'Stimuli Type', choices=STIMULI_TYPE_CHOICE, max_length=20, default=WORD_LIST)
    experiment = models.ForeignKey(
        Experiment, related_name="stimulus", on_delete=models.CASCADE)


class WordListStimuli(models.Model):
    word_list = models.TextField(max_length=10000)
    parent_stimuli = models.OneToOneField(
        Stimuli, related_name='word_list_stimuli', on_delete=models.CASCADE)


# Create your models here.
class Contrast(models.Model):
    id = HashidAutoField(primary_key=True)
    privacy_choice = models.CharField(
        'Contrast Privacy Settings', choices=PRIVACY_CHOICES, max_length=2, default=PUBLIC)
    contrast_title = models.TextField('Contrast Title (Optional)', blank=True)
    baseline_choice = models.BooleanField('Compare to baseline', default=False)
    permutation_choice = models.BooleanField(
        'Run permutation/bootstrap test(needs more waiting time)', default=False)
    experiment = models.ForeignKey(
        Experiment, related_name="contrasts", on_delete=models.CASCADE)
    result_generated = models.BooleanField(
        'Result generated or not', default=False)
    creator = models.ForeignKey(
        User, related_name='has_contrasts', on_delete=models.CASCADE, null=True)
    hash_key = models.CharField('Hash Key', max_length=56,db_index=True)

    def serialize(self):
        if self.experiment.stimuli_type == WORD_LIST:
            return self.serialize_in_word_list()

    def serialize_in_word_list(self):
        conditions = self.conditions.all()
        condition1, condition2 = None, None
        if len(conditions) == 2:
            condition1 = conditions[0]
            condition2 = conditions[1]
        else:
            # raise error message
            return None
        list1_name = condition1.condition_name
        list2_name = condition2.condition_name
        list1_text = get_word_list_condition_text(condition1)
        list2_text = get_word_list_condition_text(condition2)

        # construct contrast dict
        contrast_dict = {}
        contrast_dict['list1_name'] = list1_name
        contrast_dict['list2_name'] = list2_name
        contrast_dict['list1'] = list1_text
        contrast_dict['list2'] = list2_text
        contrast_dict['do_perm'] = contrast.permutation_choice
        contrast_dict['c_id'] = str(contrast.id)
        contrast_dict['contrast_title'] = contrast.contrast_title
        contrast_dict['result_generated'] = contrast.result_generated
        contrast_dict['stimuli_type'] = WORD_LIST
        contrast_dict['coordinate_space'] = contrast.experiment.coordinate_space
        contrast_dict['model_type'] = contrast.experiment.model_type
        return contrast_dict



class Subject_Result(models.Model):
    name = models.TextField('Subject Name', null=False, max_length=50)
    contrast = models.ForeignKey(
        Contrast, related_name="subject_results", on_delete=models.CASCADE)


class Analysis_Result(models.Model):
    name = models.TextField('Analysis Name', null=False, max_length=50)
    subject = models.ForeignKey(
        Subject_Result, related_name="analyses", on_delete=models.CASCADE)
    result = models.TextField('Analysis Result', null=False)

class Condition(models.Model):
    condition_name = models.TextField('Condition name', max_length=50)
    stimulus = models.ManyToManyField(Stimuli, through='ConditionCombination',
                                      through_fields=('condition', 'stimuli'))
    contrast = models.ForeignKey(
        Contrast, related_name="conditions", on_delete=models.CASCADE)


class ConditionCombination(models.Model):
    stimuli = models.ForeignKey(Stimuli, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)


class Coordinate(models.Model):
    coordinate_name = models.TextField('roi name', max_length=50)
    x = models.IntegerField('x')
    y = models.IntegerField('y')
    z = models.IntegerField('z')
    contrast = models.ForeignKey(Contrast, on_delete=models.CASCADE)
    # coordinates_holder = models.ForeignKey(Coordinates_holder)

# for coordinate analysis
# class Coordinates_holder(models.Model):
#     title = models.TextField('', default = '')
#     roi_image_filename = models.TextField('',  default = '')
#     allmasks = models.TextField('',  default = '')
#     contrast = models.ForeignKey(Contrast,on_delete=models.CASCADE)
