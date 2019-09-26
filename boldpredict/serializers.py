from rest_framework import serializers
from boldpredict.models import*
from boldpredict.constants import *
from boldpredict.api import stimuli_api

class StimuliSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    stimuli_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    stimuli_type = serializers.CharField(max_length=20)
    stimuli_content = serializers.CharField(max_length=10000)
    exp_id = serializers.IntegerField()
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        stimuli = stimuli_api.create_stimuli(**validated_data)
        return stimuli

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance