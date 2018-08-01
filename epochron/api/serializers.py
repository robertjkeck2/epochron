import uuid

from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        job = Job.objects.create(**validated_data)
        return job

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('daily_usage', 'previous_run_duration', 'user')
