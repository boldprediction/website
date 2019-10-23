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
        user = User.objects.create(username='test',password="test")
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
        self.stimuli_data = {'exp_id': self.exp_id, 'stimuli_content': "walk, run, smile", "stimuli_name": "actions",
                             "stimuli_type": "word_list"}

    def test_stimuli_creation(self):
        response = self.api_client.post(
            self.stimuli_url, self.stimuli_data, format='json')
        assert response.status_code == 201
        response_data = response.data
        stimuli_id = response_data['id']
        assert response_data['stimuli_type'] == "word_list"
        assert response_data['stimuli_content'] == "walk, run, smile"
        assert response_data['stimuli_name'] == "actions"

        response = self.api_client.delete(
            '/api/stimuli/' + str(stimuli_id), {}, format='json')
        response_data = response.data
        assert response.status_code == 200
        assert response_data['id'] == stimuli_id

    def test_experiment_detail(self):
        response = self.api_client.get(
            '/api/experiment/' + str(self.exp_id), {}, format='json')
        response_data = response.data
        assert response_data['stimuli_type'] == WORD_LIST
        assert response_data['coordinate_space'] == MNI
        assert response_data['experiment_title'] == 'test experiment'
        assert response_data['model_type'] == WORD2VEC
        assert response_data['authors'] == 'vivi'


class ContrastAPITestCase(TestCase):
    def setUp(self):
        self.api_client = APIClient(enforce_csrf_checks=True)
        self.input_params = {'model_type': ENG1000,
                             'stimuli_type': WORD_LIST,
                             'coordinate_space': MNI,
                             'list1_name': 'fruit',
                             'list1_text': 'apple, peach, grapes',
                             'list2_name': 'action',
                             'list2_text': 'run, walk, smile',
                             'contrast_type': PUBLIC,
                             'contrast_title': 'contrast test',
                             }

    def test_contrast_creation(self):
        response = self.api_client.post(
            '/api/create_contrast', self.input_params, format='json')
        assert response.status_code == 200
        contrast_id = json.loads(response.content)['contrast_id']
        # if Contrast.objects.get(id = contrast_id):
        #     print("find contrast")
        # else:
        #     print("not find")
        # self.update_info = [
        #     {
        #         "contrast_info": {
        #             'id': str(contrast_id)
        #         },
        #         "group_analyses": "test analysis",
        #         "subjects_analyses": "test subjects"
        #     }
        # ]

        # print("contrast_id  = ", contrast_id)
        # response = self.api_client.post(
        #     '/api/update_contrast', self.update_info, format='json')
        # contrast_ids = json.loads(response.content)['contrast_ids']
        # assert contrast_id in contrast_ids
