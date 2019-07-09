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


def create_word_list_contrast(*args, **kwargs):
    # experiment attributes
    print("start creating contrast")
    title = kwargs.get('experiment_title', None)
    authors = kwargs.get('authors', None)
    DOI = kwargs.get('DOI', None)
    model_type = kwargs.get('model_type', ENG1000)
    stimuli_type = kwargs.get('stimuli_type', WORD_LIST)
    coordinate_space = kwargs.get('coordinate_space', MNI)
    exp = Experiment.objects.create(experiment_title=title, authors=authors,
                                    DOI=DOI, model_type=model_type, stimuli_type=stimuli_type,
                                    coordinate_space=coordinate_space)
    # exp = Experiment.objects.create(title=title)
    print("experiment successfully saved, experiment id = ", exp.id)

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
    contrast_title = kwargs.get('contrast_title', None)
    baseline_choice = kwargs.get('baseline_choice', False)
    permutation_choice = kwargs.get('permutation_choice', False)
    contrast = Contrast.objects.create(contrast_title=contrast_title,
                                       experiment=exp, baseline_choice=baseline_choice,
                                       permutation_choice=permutation_choice,
                                       privacy_choice=contrast_type)

    # create condition
    condition1 = Condition.objects.create(
        condition_name=list1_name, contrast=contrast)
    # condition1.stimulus.set([stimuli1])
    combine1 = ConditionCombination.objects.create(stimuli = stimuli1,condition = condition1)
    condition2 = Condition.objects.create(
        condition_name=list2_name, contrast=contrast)
    combine2 = ConditionCombination.objects.create(stimuli = stimuli2,condition = condition2)
    # condition1.stimulus.set([stimuli2])

    return contrast
