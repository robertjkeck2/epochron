import uuid

from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        job = Job.objects.create(**validated_data)
        if job.user:
            job.user.num_jobs = job.user.num_jobs + 1
            job.user.save()
        return job

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('daily_usage', 'last_run_duration', 'user')
