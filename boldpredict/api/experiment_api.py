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
                                    coordinate_space=coordinate_space)
    
    return exp.serialize()

def get_experiment(exp_id):
    pass
