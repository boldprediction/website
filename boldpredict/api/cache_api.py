from boldpredict.constants import *


def update_word_list_cache_record(key1,key2,mni_str,subj_str):
    pass 

def update_contrast_record(contrast_dict, mni_str, subj_str):
    stimuli_type = contrast_dict['stimuli_type']
    if stimuli_type == WORD_LIST:
        update_word_list_contrast_record(contrast_dict,mni_str,subj_str)

def update_word_list_contrast_record(contrast_dict,mni_str,subj_str):
    key1 = contrast_dict['list1']
    key2 = contrast_dict['list2']
    record = update_word_list_cache_record(key1,key2,mni_str,subj_str)


