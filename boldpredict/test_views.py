from django.test import TestCase

# Create your tests here.
from boldpredict.api import experiment_api, contrast_api, cache_api, stimuli_api, sqs_api
from boldpredict.constants import *
import boldpredict.utils as utils
from django.contrib.auth.models import User
from boldpredict.models import Contrast
from rest_framework.test import APIClient
from django.urls import reverse
import json

# https://www.django-rest-framework.org/api-guide/testing/#forcing-authentication


class ExperimentCreationAPITestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='test', password="test")
        self.api_client = APIClient(enforce_csrf_checks=True)
        self.api_client.force_authenticate(user=user)
        self.input_params = {'model_type': WORD2VEC,
                             'stimuli_type': WORD_LIST,
                             'coordinate_space': MNI,
                             'experiment_title': 'test experiment',
                             'authors': 'vivi',
                             'DOI': '10.1162/0898929054021102',
                             'is_published': True
                             }
        experiment = experiment_api.create_experiment(**self.input_params)
        self.exp_id = experiment.id
        self.stimuli_url = "/api/stimuli"
        self.stimuli_data1 = {'exp_id': self.exp_id, 'stimuli_content': "walk, run, smile", "stimuli_name": "actions",
                              "stimuli_type": "word_list"}
        self.stimuli_data2 = {'exp_id': self.exp_id, 'stimuli_content': "grape, apple, rice", "stimuli_name": "food",
                              "stimuli_type": "word_list"}

    # test_stimuli_creation(self):
        response = self.api_client.post(
            self.stimuli_url, self.stimuli_data1, format='json')
        assert response.status_code == 201
        response_data = response.data
        self.stimuli_id1 = response_data['id']
        assert response_data['stimuli_type'] == "word_list"
        assert response_data['stimuli_content'] == "walk, run, smile"
        assert response_data['stimuli_name'] == "actions"

        response = self.api_client.post(
            self.stimuli_url, self.stimuli_data2, format='json')
        assert response.status_code == 201
        response_data = response.data
        self.stimuli_id2 = response_data['id']
        assert response_data['stimuli_type'] == "word_list"
        assert response_data['stimuli_content'] == "grape, apple, rice"
        assert response_data['stimuli_name'] == "food"

    def test_contrast_list(self):
        id1 = str(self.stimuli_id1)
        id2 = str(self.stimuli_id2)
        contrast_data = [
            {
                "baseline_choice": False,
                "permutation_choice": False,
                "privacy_choice": "PR",
                "contrast_name": "contrast1",
                "condition1": {
                    "name": "condition1name",
                    "stimuli_list": [
                        id1
                    ]
                },
                "condition2": {
                    "name": "condition2name",
                    "stimuli_list": [
                        id2
                    ]
                },
                "coordinates": [
                    {
                        "name": "L posterior middle temporal gyrus",
                        "x": "-63",
                        "y": "-42",
                        "z": "-3",
                        "zscore": "4.48"
                    },
                    {
                        "name": "L anterior fusiform gyrus",
                        "x": "-45",
                        "y": "-42",
                        "z": "12",
                        "zscore": "3.74"
                    }
                ],
                "figures": [
                    "images/Davis2004/Davis2004Figure1.pdf"
                ]
            }]
        response = self.api_client.post(
            '/api/contrasts/' + str(self.exp_id), contrast_data, format='json')
        response_data = response.data
        contrast_ids = response_data['contrast_ids']

        get_response = self.api_client.get(
            '/api/contrasts/' + str(self.exp_id), {}, format='json')
        
        contrasts = get_response.data
        for contrast in contrasts:
            assert contrast['id'] in contrast_ids

    def test_experiment_detail(self):
        response = self.api_client.get(
            '/api/experiment/' + str(self.exp_id), {}, format='json')
        response_data = response.data
        assert response_data['stimuli_type'] == WORD_LIST
        assert response_data['coordinate_space'] == MNI
        assert response_data['experiment_title'] == 'test experiment'
        assert response_data['model_type'] == WORD2VEC
        assert response_data['authors'] == 'vivi'

    def test_stimuli_deletion(self):
        response = self.api_client.delete(
            '/api/stimuli/' + str(self.stimuli_id1), {}, format='json')
        response_data = response.data
        assert response.status_code == 200
        assert response_data['id'] == self.stimuli_id1



class ContrastAPITestCase(TestCase):
    def setUp(self):
        self.api_client = APIClient(enforce_csrf_checks=True)
        self.input_params = {'model_type': ENG1000,
                             'stimuli_type': WORD_LIST,
                             'coordinate_space': MNI,
                             'list1_name': 'fruit',
                             'list1_text': 'apple, peach, grapes',
                             'list2_name': 'action',
                             'list2_text': 'run, walk, smile, cry',
                             'contrast_type': PUBLIC,
                             'contrast_title': 'contrast test',
                             }

    def test_contrast_creation(self):
        c_id, find, hash_key = contrast_api.check_existing_contrast(
            **self.input_params)
        if find:
            cache_api.delete_contrast_in_cache(c_id, hash_key)

        response = self.api_client.post(
            '/api/create_contrast', self.input_params, format='json')

        assert response.status_code == 200
        contrast_id = json.loads(response.content)['contrast_id']
        contrast_hash_key = json.loads(response.content)['hash_key']

        if Contrast.objects.get(id=contrast_id):
            print("find contrast")
        else:
            print("not find")
        self.update_info = [
            {
                "contrast_info": {
                    'id': str(contrast_id)
                },
                "group_analyses": {"A": "group_analysisa"},
                "subjects_analyses":  {"subjectA": {"result1": "subject_analysis"}}
            }
        ]
        response = self.api_client.post(
            '/api/update_contrast', self.update_info, format='json')
        contrast_ids = json.loads(response.content)['contrast_ids']
        cache_api.delete_contrast_in_cache(contrast_id, contrast_hash_key)
        assert contrast_id in contrast_ids
