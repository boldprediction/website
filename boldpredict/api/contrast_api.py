from boldpredict.models import *
from boldpredict.constants import *


def create_contrast():
    pass


def create_condition():
    pass


def create_word_list_stimuli(stimuli_type, name, text, exp):
    stimuli = Stimuli.objects.create(stimuli_name=name, stimuli_type=stimuli_type,
                                     experiment=exp)
    word_list_stimuli = WordListStimuli.objects.create(
        word_list=text, parent_stimuli=stimuli)

    return stimuli, word_list_stimuli


def create_single_word_list_contrast(*args, **kwargs):
    # experiment attributes
    title = kwargs.get('experiment_title', None)
    authors = kwargs.get('authors', None)
    DOI = kwargs.get('DOI', None)
    model_type = kwargs.get('model_type', ENG1000)
    stimuli_type = kwargs.get('stimuli_type', WORD_LIST)
    coordinate_space = kwargs.get('coordinate_space', MNI)
    exp = Experiment.objects.create(experiment_title=title, authors=authors,
                                    DOI=DOI, model_type=model_type, stimuli_type=stimuli_type,
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
    contrast_title = kwargs.get('contrast_title', list1_name + '-' + list2_name)
    if len(contrast_title) == 0:
        contrast_title = list1_name + '-' + list2_name
    baseline_choice = kwargs.get('baseline_choice', False)
    permutation_choice = kwargs.get('permutation_choice', False)
    contrast = Contrast.objects.create(contrast_title=contrast_title,
                                       experiment=exp, baseline_choice=baseline_choice,
                                       permutation_choice=permutation_choice,
                                       privacy_choice=contrast_type)

    # create condition
    condition1 = Condition.objects.create(
        condition_name=list1_name, contrast=contrast)
    combine1 = ConditionCombination.objects.create(stimuli = stimuli1,condition = condition1)
    condition2 = Condition.objects.create(
        condition_name=list2_name, contrast=contrast)
    combine2 = ConditionCombination.objects.create(stimuli = stimuli2,condition = condition2)

    return contrast


def get_word_list_condition_text(condition):
    text = ""
    stimulus = condition.stimulus.all()
    word_lists = [stimuli.word_list_stimuli.word_list for stimuli in stimulus]
    text = ','.join(word_lists)
    print("text = ", text)
    print("word_lists = ", word_lists)
    return text

def get_word_list_contrast(contrast_id):
    contrast = Contrast.objects.get( id = contrast_id )
    print("contrast conditions = ",contrast.conditions)
    conditions = contrast.conditions.all()
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
    contrast_dict  = {}
    contrast_dict['list1_name'] = list1_name
    contrast_dict['list2_name'] = list2_name
    contrast_dict['list1'] = list1_text
    contrast_dict['list2'] = list2_text
    contrast_dict['do_perm'] = contrast.permutation_choice
    contrast_dict['c_id'] = contrast.id
    contrast_dict['contrast_title'] = contrast.contrast_title
    return contrast_dict

def get_contrast_mni_str(contrast_id):
    contrast = Contrast.objects.get( id = contrast_id )
    mni_dict =  {}
    mni_dict['Cstr'] = contrast.MNIstr
    return mni_dict

def get_contrast_subj_str(contrast_id,subj_num):
    contrast = Contrast.objects.get( id = contrast_id )
    sub_dict =  {}
    mni_dict['Cstr'] = jsonDec.decode(contrast.subjstr)[subj_num - 1]
    mni_dict['c_id'] = contrast.id
    return mni_dict