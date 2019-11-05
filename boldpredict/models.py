from django.contrib.auth.models import User
from django.db import models
from hashid_field import HashidAutoField
from boldpredict.constants import *
from django.utils import timezone
import json


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

    is_published = models.BooleanField(
        'Is this a published experiment', default=False)

    # is_approved = models.BooleanField(
    #     'If it is a published experiment, is this experiment approved', default=False)

    status = models.CharField(
        'Stimuli Type', choices=STATUS_CHOICE, max_length=20, default=CREATED)

    def serialize(self):
        return {
            "id": self.id,
            "experiment_title": self.experiment_title,
            "authors": self.authors,
            "DOI": self.DOI,
            "creator": self.creator.username if self.creator is not None else "",
            "stimuli_type": self.stimuli_type,
            "coordinate_space": self.coordinate_space,
            "model_type": self.model_type,
            "is_published": self.is_published,
            # "is_approved": self.is_approved,
            "status": self.status,
            "stimuli": [stimuli.serialize() for stimuli in self.stimulus.all()]
        }


class Stimuli(models.Model):
    stimuli_name = models.TextField('name of stimuli', max_length=50)
    stimuli_type = models.CharField(
        'Stimuli Type', choices=STIMULI_TYPE_CHOICE, max_length=20, default=WORD_LIST)
    experiment = models.ForeignKey(
        Experiment, related_name="stimulus", on_delete=models.CASCADE)

    def serialize(self):
        if self.stimuli_type == WORD_LIST:
            return {
                "id": self.id,
                "stimuli_type": self.stimuli_type,
                "stimuli_name": self.stimuli_name,
                "stimuli_content": self.word_list_stimuli.word_list if hasattr(self, 'word_list_stimuli') else ""
            }


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
    hash_key = models.CharField('Hash Key', max_length=56, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    result_generated_at = models.DateTimeField(null=True)
    figures_list = models.TextField('Contrast related figures', default='[]')

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

        condition1_dict = condition1.serialize()
        condition2_dict = condition2.serialize()
        list1_name = condition1_dict['name']
        list2_name = condition2_dict['name']
        list1_text = condition1_dict['list_text']
        list2_text = condition2_dict['list_text']

        # construct contrast dict
        contrast_dict = {}
        contrast_dict['privacy_choice'] = self.privacy_choice
        contrast_dict['baseline_choice'] = self.baseline_choice
        contrast_dict['list1_name'] = list1_name
        contrast_dict['list2_name'] = list2_name
        contrast_dict['list1'] = list1_text
        contrast_dict['list2'] = list2_text
        contrast_dict['do_perm'] = self.permutation_choice
        contrast_dict['c_id'] = str(self.id)
        contrast_dict['contrast_title'] = self.contrast_title
        contrast_dict['result_generated'] = self.result_generated
        contrast_dict['stimuli_type'] = WORD_LIST
        contrast_dict['coordinate_space'] = self.experiment.coordinate_space
        contrast_dict['model_type'] = self.experiment.model_type
        contrast_dict['hash_key'] = self.hash_key
        contrast_dict['created_at'] = str(self.created_at)
        contrast_dict['result_generated_at'] = str(self.result_generated_at)
        contrast_dict['figures_list'] = self.figures_list
        contrast_dict['figure_num'] = len(json.loads(
            self.figures_list)) if len(self.figures_list) != 0 else 0

        # collect subjects result
        subjects_dict = {}
        subjects = self.subjects.all()
        for subject in subjects:
            subjects_dict[subject.name] = subject.serialize()
        contrast_dict['subjects'] = subjects_dict

        return contrast_dict


class Subject_Result(models.Model):
    name = models.TextField('Subject Name', null=False, max_length=50)
    contrast = models.ForeignKey(
        Contrast, related_name="subjects", on_delete=models.CASCADE)

    def serialize(self):
        subject_dict = {}
        analyses = self.analyses.all()
        for analysis in analyses:
            subject_dict[analysis.name] = analysis.result
        return subject_dict


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

    def serialize(self):
        if self.contrast.experiment.stimuli_type == WORD_LIST:
            return self.serialize_in_word_list()

    def serialize_in_word_list(self):
        condition_dict = {}
        condition_dict['name'] = self.condition_name
        text = ""
        stimulus = self.stimulus.all()
        word_lists = [
            stimuli.word_list_stimuli.word_list for stimuli in stimulus]
        text = ','.join(word_lists)
        condition_dict['list_text'] = text
        return condition_dict


class ConditionCombination(models.Model):
    stimuli = models.ForeignKey(Stimuli, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)


class Coordinate(models.Model):
    coordinate_name = models.TextField('roi name', max_length=50)
    x = models.FloatField('x')
    y = models.FloatField('y')
    z = models.FloatField('z')
    contrast = models.ForeignKey(Contrast, on_delete=models.CASCADE, related_name="coordinates")
    zscore = models.FloatField('zscore',null=True)
    tscore = models.FloatField('tscore',null=True)
    voxel = models.FloatField('voxel',null=True)
    # coordinates_holder = models.ForeignKey(Coordinates_holder)

# for coordinate analysis
# class Coordinates_holder(models.Model):
#     title = models.TextField('', default = '')
#     roi_image_filename = models.TextField('',  default = '')
#     allmasks = models.TextField('',  default = '')
#     contrast = models.ForeignKey(Contrast,on_delete=models.CASCADE)
