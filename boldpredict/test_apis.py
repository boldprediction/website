
# https://docs.djangoproject.com/en/2.2/topics/testing/advanced/
# https://docs.djangoproject.com/en/2.2/topics/testing/overview/

from django.test import TestCase

# Create your tests here.
from boldpredict.api import experiment_api,contrast_api,cache_api
from boldpredict.constants import *
import boldpredict.utils as utils
from boldpredict.models import Contrast


class ExperimentTestCase(TestCase):
    def setUp(self):
        self.input_params = {'model_type': WORD2VEC,
                        'stimuli_type': IMAGE,
                        'coordinate_space': MNI,
                        'experiment_title': 'test experiment',
                        'authors': 'vivi',
                        'DOI': '10.1162/0898929054021102',
                        'is_published': True
                        }

    def test_experiment_creation(self):
        experiment = experiment_api.create_experiment(**self.input_params)
        exp_id = experiment.id
        exp = experiment_api.get_experiment(exp_id)
        self.assertEqual(exp.authors, 'vivi')
        self.assertEqual(exp.model_type, WORD2VEC)
        self.assertEqual(exp.stimuli_type, IMAGE)
        self.assertEqual(exp.coordinate_space, MNI)
        self.assertEqual(exp.DOI, '10.1162/0898929054021102')
        self.assertEqual(exp.is_published, True)

class ContrastTestCase(TestCase):
    def setUp(self):
        self.exp_input_params = {'model_type': ENG1000,
                        'stimuli_type': WORD_LIST,
                        'coordinate_space': MNI,
                        'experiment_title': 'test experiment',
                        'authors': 'vivi',
                        'DOI': '10.1162/0898929054021102',
                        'is_published': True
                        }

        self.input_params = {'model_type': ENG1000,
                        'stimuli_type': WORD_LIST,
                        'coordinate_space': MNI,
                        'list1_name': 'fruit',
                        'list1_text': 'apple, peach, grapes',
                        'list2_name': 'action',
                        'list2_text': 'run, walk, smile',
                        'contrast_type': PUBLIC,
                        'contrast_title' : 'contrast test',
                        }
        
        # self.no_cache_input_params = {'model_type': ENG1000,
        #         'stimuli_type': WORD_LIST,
        #         'coordinate_space': MNI,
        #         'list1_name': 'fruit',
        #         'list1_text': 'apple, peach, grapes, blueberries',
        #         'list2_name': 'action',
        #         'list2_text': 'run, walk, smile, cry, pat',
        #         'contrast_type': PUBLIC,
        #         'contrast_title' : 'contrast test',
        #         }
        contrast = contrast_api.create_contrast(**self.input_params)
        self.contrast_id = contrast.id
        self.hash_key = contrast.hash_key

    def test_contrast_creation(self):
        contrast_dict1 = contrast_api.get_contrast_dict_by_id(self.contrast_id)
        contrast_dict2 = contrast_api.get_contrast_dict_by_hash_key(str(self.hash_key))
        self.assertEqual(contrast_dict1['model_type'], ENG1000)
        self.assertEqual(contrast_dict2['model_type'], ENG1000)
        self.assertEqual(contrast_dict1['stimuli_type'], WORD_LIST)
        self.assertEqual(contrast_dict2['stimuli_type'], WORD_LIST)
        self.assertEqual(contrast_dict1['coordinate_space'], MNI)
        self.assertEqual(contrast_dict2['coordinate_space'], MNI)
        self.assertEqual(contrast_dict1['list1_name'], 'fruit')
        self.assertEqual(contrast_dict2['list1_name'], 'fruit')
        self.assertEqual(contrast_dict1['list1'], 'apple, peach, grapes')
        self.assertEqual(contrast_dict2['list1'], 'apple, peach, grapes')
        self.assertEqual(contrast_dict1['hash_key'], self.hash_key)
        self.assertEqual(contrast_dict2['c_id'], self.contrast_id)
    
    def test_contrast_without_cache(self):
        cache_api.delete_contrast_in_cache(self.contrast_id,self.hash_key)
        contrast_dict1 = contrast_api.get_contrast_dict_by_id(self.contrast_id)
        cache_api.delete_contrast_in_cache(self.contrast_id,self.hash_key)
        contrast_dict2 = contrast_api.get_contrast_dict_by_hash_key(str(self.hash_key))
        self.assertEqual(contrast_dict1['model_type'], ENG1000)
        self.assertEqual(contrast_dict2['model_type'], ENG1000)
        self.assertEqual(contrast_dict1['stimuli_type'], WORD_LIST)
        self.assertEqual(contrast_dict2['stimuli_type'], WORD_LIST)
        self.assertEqual(contrast_dict1['coordinate_space'], MNI)
        self.assertEqual(contrast_dict2['coordinate_space'], MNI)
        self.assertEqual(contrast_dict1['list1_name'], 'fruit')
        self.assertEqual(contrast_dict2['list1_name'], 'fruit')
        self.assertEqual(contrast_dict1['list1'], 'apple, peach, grapes')
        self.assertEqual(contrast_dict2['list1'], 'apple, peach, grapes')
        self.assertEqual(contrast_dict1['hash_key'], self.hash_key)
        self.assertEqual(contrast_dict2['c_id'], self.contrast_id)

        # experiment = experiment_api.create_experiment(**self.exp_input_params)
        # hash_key = utils.generate_hash_key(**self.no_cache_input_params)
        # print("hash key = ", hash_key)
        # contrast = Contrast.objects.create(contrast_title='title', experiment = experiment,
        #                                privacy_choice=PUBLIC, hash_key = hash_key)
        # contrast_id = contrast.id
        # print("contrast_id = ", contrast_id, " contrast hash_key = ", hash_key)
        # contrast_dict1 = contrast_api.get_contrast_dict_by_id(contrast_id)
        # contrast_dict2 = contrast_api.get_contrast_dict_by_hash_key(hash_key)
        # self.assertEqual(contrast_dict1['hash_key'], hash_key)
        # self.assertEqual(contrast_dict1['model_type'], ENG1000)
        # self.assertEqual(contrast_dict2['model_type'], ENG1000)
        # self.assertEqual(contrast_dict1['stimuli_type'], WORD_LIST)
        # self.assertEqual(contrast_dict2['stimuli_type'], WORD_LIST)
        # self.assertEqual(contrast_dict1['coordinate_space'], MNI)
        # self.assertEqual(contrast_dict2['coordinate_space'], MNI)
        # self.assertEqual(contrast_dict2['c_id'], contrast_id)