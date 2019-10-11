from django.test import TestCase

# Create your tests here.
from boldpredict.api import experiment_api, contrast_api, cache_api, stimuli_api, sqs_api
from boldpredict.constants import *
import boldpredict.utils as utils
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.test import Client
from django.urls import reverse

# https://www.django-rest-framework.org/api-guide/testing/#forcing-authentication
class ExperimentCreationAPITestCase(TestCase):
    def setUp(self):
        # view_client = Client()
        self.api_client = APIClient(enforce_csrf_checks=True)
        # self.api_client.force_authenticate(user=user)
        # self.api_client.login(username='testuser', password='testuser123')
        # self.exp_url = "new_experiment"
        # self.exp_args = {"experiment_title": "test experiment", "authors": "vivi",
        #                  "DOI": "abcd", "coordinate_space": "MNI", 
        #                  "stimuli_type": "word_list", "model_type": "english1000"}
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
        response = self.api_client.post(self.stimuli_url, self.stimuli_data, format='json')
        assert response.status_code == 201
        response_data  = response.data
        assert response_data['stimuli_type'] == "word_list"
        assert response_data['stimuli_content'] == "walk, run, smile"
        assert response_data['stimuli_name'] == "actions"

    def test_experiment_detail(self):
        response = self.api_client.get('/api/experiment/'+ str(self.exp_id), {} , format='json')
        response_data  = response.data
        assert response_data['stimuli_type'] == WORD_LIST
        assert response_data['coordinate_space'] == MNI
        assert response_data['experiment_title'] == 'test experiment'
        assert response_data['model_type'] == WORD2VEC
        assert response_data['authors'] == 'vivi'
