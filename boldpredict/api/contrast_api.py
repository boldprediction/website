from boldpredict.models import *
from boldpredict.constants import *
import json
from django.conf import settings
from boldpredict.api import cache_api
import boldpredict.utils as utils


def create_word_list_stimuli(stimuli_type, name, text, exp):
    stimuli = Stimuli.objects.create(stimuli_name=name, stimuli_type=stimuli_type,
                                     experiment=exp)
    word_list_stimuli = WordListStimuli.objects.create(
        word_list=text, parent_stimuli=stimuli)

    return stimuli, word_list_stimuli

def create_word_list_contrast(*args, **kwargs):

    hash_key = kwargs.get('hash_key', None)
    if hash_key is None:
        hash_key = utils.generate_hash_key(**kwargs)

    model_type = kwargs.get('model_type', ENG1000)
    stimuli_type = kwargs.get('stimuli_type', WORD_LIST)
    coordinate_space = kwargs.get('coordinate_space', MNI)

    # experiment attributes
    title = kwargs.get('experiment_title', None)
    authors = kwargs.get('authors', None)
    DOI = kwargs.get('DOI', None)
    owner = kwargs.get('owner', None)
    exp = Experiment.objects.create(experiment_title=title, authors=authors,
                                    DOI=DOI, creator = owner, model_type=model_type,
                                    stimuli_type=stimuli_type,
                                    coordinate_space=coordinate_space)

    # create stimuli
    list1_name = kwargs.get('list1_name', None)
    list1_text = kwargs.get('list1_text', None)
    stimuli1, word_list_stimuli_1 = create_word_list_stimuli(
        stimuli_type, list1_name, list1_text, exp)
    list2_name = kwargs.get('list2_name', None)
    list2_text = kwargs.get('list2_text', None)
    stimuli2, word_list_stimuli_2 = create_word_list_stimuli(
        stimuli_type, list2_name, list2_text, exp)

    # contrast
    contrast_type = kwargs.get('contrast_type', PUBLIC)
    contrast_title = kwargs.get(
        'contrast_title', list1_name + '-' + list2_name)
    if len(contrast_title) == 0:
        contrast_title = list1_name + '-' + list2_name
    baseline_choice = kwargs.get('baseline_choice', False)
    permutation_choice = kwargs.get('permutation_choice', False)
    contrast = Contrast.objects.create(contrast_title=contrast_title, baseline_choice=baseline_choice,
                                       permutation_choice=permutation_choice, experiment = exp,
                                       privacy_choice=contrast_type, creator = owner,
                                       hash_key = hash_key )

    # create condition
    condition1 = Condition.objects.create(
        condition_name=list1_name, contrast=contrast)
    combine1 = ConditionCombination.objects.create(
        stimuli=stimuli1, condition=condition1)
    condition2 = Condition.objects.create(
        condition_name=list2_name, contrast=contrast)
    combine2 = ConditionCombination.objects.create(
        stimuli=stimuli2, condition=condition2)

    cache_api.add_contrast_into_cache(hash_key,contrast.serialize())
    cache_api.add_contrast_into_cache(str(contrast.id),contrast.serialize())
    return contrast


def update_contrast_result(contrast_id,group_analyses,subjects):
    contrast = Contrast.objects.get(id = contrast_id)
    # create subject for mni - group result
    mni_subject = Subject_Result.objects.create(name = 'MNI',contrast = contrast)
    for analysis_name, result in group_analyses.items():
        analysis = Analysis_Result.objects.create(name = analysis_name, result = result, subject = mni_subject)
    
    # create subject for other subjects - group result
    for subject_name, subject_analyses in subjects.items():
        subject = Subject_Result.objects.create(name = subject_name,contrast = contrast)
        for analysis_name, result in subject_analyses.items():
            analysis = Analysis_Result.objects.create(name = analysis_name, result = result, subject = subject)
    
    contrast.result_generated = True
    contrast.save()

    cache_api.update_contrast_in_cache(str(contrast.id),contrast.serialize())
    cache_api.update_contrast_in_cache(contrast.hash_key,contrast.serialize())


def get_contrast_dict_by_hash_key(hash_key):
    ext_contrast = cache_api.check_contrast_in_cache(hash_key)
    if ext_contrast :
        return ext_contrast
    try:
        contrast = Contrast.objects.get(hash_key=hash_key)
        return contrast.serialize()
    except:
        return None


def get_contrast_dict_by_id(contrast_id):
    ext_contrast = cache_api.check_contrast_in_cache(str(contrast_id))
    if ext_contrast :
        return ext_contrast
    try:
        contrast = Contrast.objects.get(id=contrast_id)
        return contrast.serialize()
    except:
        return None


def get_contrast_subj_webgl_strs(contrast_id, subj_name):
    analysis = Analysis_Result.objects.filter( subject__contrast__id =  contrast_id).filter( subject__name = subj_name ).filter( name__startswith = 'webgl' ).all()
    if analysis and len(analysis) > 0:
        return analysis[0].result
    return ""
    

def check_existing_contrast(*args, **kwargs):
    hash_key = utils.generate_hash_key(**kwargs)
    contrast_dict = get_contrast_dict_by_hash_key(hash_key)
    if contrast_dict:
        return contrast_dict['c_id'], True, hash_key
    return None, False , hash_key

