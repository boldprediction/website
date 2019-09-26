from boldpredict.api import experiment_api
from boldpredict.constants import *
from boldpredict.models import Stimuli,WordListStimuli
def create_word_list_stimuli(stimuli_type, name, text, exp):
    stimuli = Stimuli.objects.create(stimuli_name=name, stimuli_type=stimuli_type,
                                     experiment=exp)
    print("stimuli = ", stimuli)
    word_list_stimuli = WordListStimuli.objects.create(
        word_list=text, parent_stimuli=stimuli)

    return stimuli, word_list_stimuli


def create_stimuli(*args, **kwargs):
    exp_id = kwargs.get('exp_id', None)
    if  exp_id is None:
        return None
    exp = experiment_api.get_experiment(exp_id)
    stimuli_type = kwargs.get('stimuli_type', WORD_LIST)
    name = kwargs.get('stimuli_name', None)
    content = kwargs.get('stimuli_content', None)
    if stimuli_type == WORD_LIST:
        stimuli, word_list_stimuli = create_word_list_stimuli(stimuli_type,name,content, exp)
        return stimuli


