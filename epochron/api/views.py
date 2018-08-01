from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Job
from .permissions import IsOwnerOrAdmin
from .serializers import JobSerializer


class JobViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves jobs
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.cron_minute = request.data.get('cron_minute', '*')
        instance.cron_hour = request.data.get('cron_hour', '*')
        instance.cron_day = request.data.get('cron_day', '*')
        instance.cron_month = request.data.get('cron_month', '*')
        instance.cron_weekday = request.data.get('cron_weekday', '*')
        instance.cron_expression = request.data.get('cron_expression', '')
        instance.save()

        serializer = JobSerializer(instance)
        return Response(serializer.data)

class JobCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates jobs
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (IsAuthenticated,)
