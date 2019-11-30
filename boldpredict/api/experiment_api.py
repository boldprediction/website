from boldpredict.models import *
from boldpredict.constants import *


def create_experiment(*args, **kwargs):
    model_type = kwargs.get('model_type', ENG1000)
    stimuli_type = kwargs.get('stimuli_type', WORD_LIST)
    coordinate_space = kwargs.get('coordinate_space', MNI)
    title = kwargs.get('experiment_title', None)
    authors = kwargs.get('authors', None)
    DOI = kwargs.get('DOI', None)
    creator = kwargs.get('creator', None)
    is_published =  kwargs.get('is_published', False)
    exp = Experiment.objects.create(experiment_title=title, authors=authors,
                                    DOI=DOI, creator = creator, model_type=model_type,
                                    stimuli_type=stimuli_type,
                                    coordinate_space=coordinate_space,
                                    is_published = is_published)
    
    return exp

def update_experiment(*args, **kwargs):
    exp_id = kwargs.get('exp_id',None)
    if exp_id is None:
        return None
    exp = Experiment.objects.get(id = exp_id)
    for key, value in kwargs.items():
        if hasattr(exp, key):
            setattr(exp, key, value)
    
    if 'experiment_title' in kwargs:
        exp.title = kwargs['experiment_title']

    exp.save()
    return exp
    

    # model_type = kwargs.get('model_type', ENG1000)
    # stimuli_type = kwargs.get('stimuli_type', WORD_LIST)
    # coordinate_space = kwargs.get('coordinate_space', MNI)
    # title = kwargs.get('experiment_title', None)
    # authors = kwargs.get('authors', None)
    # DOI = kwargs.get('DOI', None)
    # creator = kwargs.get('creator', None)
    # is_published =  kwargs.get('is_published', False)
    # is_approved =  kwargs.get('is_approved', False)

    # exp.experiment_title = title
    # exp.authors = authors
    # exp.DOI = DOI
    # exp.creator = creator
    # exp.model_type = model_type
    # exp.stimuli_type = stimuli_type
    # exp.coordinate_space = coordinate_space
    # exp.is_published = is_published
    # exp.is_approved = is_approved
    # exp.save()
    # return exp

def get_experiment(exp_id):
    try:
        experiment = Experiment.objects.get(pk=exp_id)
        return experiment
    except Experiment.DoesNotExist:
        return None
