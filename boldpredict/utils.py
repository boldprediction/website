import hashlib
from boldpredict.constants import *

def generate_word_list_hash_key(*args, **kwargs):
    print("kwargs = ", kwargs)
    hash224 = hashlib.sha224()
    
    stimuli_type = kwargs.get('stimuli_type', WORD_LIST)
    model_type = kwargs.get('model_type', ENG1000)
    coordinate_space = kwargs.get('coordinate_space', MNI)
    owner = kwargs.get('owner', None)
    list1_text = kwargs.get('list1_text', None)
    list2_text = kwargs.get('list2_text', None)
    contrast_type = kwargs.get('contrast_type', PUBLIC)
    permutation_choice = kwargs.get('permutation_choice', False)
    hash224.update(model_type.encode('utf-8'))
    
    hash224.update(stimuli_type.encode('utf-8'))
    hash224.update(coordinate_space.encode('utf-8'))
    hash224.update(list1_text.encode('utf-8'))
    hash224.update(list2_text.encode('utf-8'))
    if permutation_choice :
        hash224.update(b'permutation choice')
    else:
        hash224.update(b'no permutation choice')

    if contrast_type == PUBLIC:
        hash224.update(b'public contrast')
    else:
        hash224.update(b'private contrast')
        hash224.update(owner.username.encode('utf-8'))

    return hash224.hexdigest()

def generate_hash_key(*args, **kwargs):
    stimuli_type = kwargs.get('stimuli_type', WORD_LIST)
    if stimuli_type == WORD_LIST:
        return generate_word_list_hash_key(*args, **kwargs)

