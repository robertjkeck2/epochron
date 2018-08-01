from datetime import datetime
import uuid

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save

from croniter import croniter
import pytz


@python_2_unicode_compatible
class Job(models.Model):
    METHOD_CHOICES = (
        ('get', 'GET'),
        ('post', 'POST'),
        ('put', 'PUT'),
        ('patch', 'PATCH'),
        ('delete', 'DELETE'),
        ('head', 'HEAD'),
        ('options', 'OPTIONS'),
    )
    TZ_CHOICES = ((tz, tz) for tz in pytz.common_timezones)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    cron_day = models.CharField(max_length=100, blank=True, default='*')
    cron_expression = models.CharField(max_length=500, blank=True, default='')
    cron_hour = models.CharField(max_length=100, blank=True, default='*')
    cron_minute = models.CharField(max_length=100, blank=True, default='*')
    cron_month = models.CharField(max_length=100, blank=True, default='*')
    cron_weekday = models.CharField(max_length=100, blank=True, default='*')
    daily_usage = models.FloatField(blank=True, default=0)
    description = models.CharField(max_length=1000, blank=True, default='')
    http_data = models.TextField(blank=True, default='')
    http_headers = models.TextField(blank=True, default='')
    http_method = models.CharField(max_length=7, choices=METHOD_CHOICES, default='get')
    http_params = models.TextField(blank=True, default='')
    http_url = models.URLField()
    previous_run_duration = models.FloatField(blank=True, default=0)
    name = models.CharField(max_length=100)
    next_run = models.DateTimeField(auto_now_add=True)
    timezone = models.CharField(max_length=100, choices=TZ_CHOICES, default='UTC')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    webhook_data = models.TextField(blank=True, default='')
    webhook_headers = models.TextField(blank=True, default='')
    webhook_method = models.CharField(max_length=7, choices=METHOD_CHOICES, default='get')
    webhook_params = models.TextField(blank=True, default='')
    webhook_url = models.URLField(blank=True, default='')

    def __str__(self):
        return self.name

@receiver(post_save, sender=settings.JOB_MODEL)
def get_next(sender, instance=None, **kwargs):
    cron_expression = instance.cron_expression
    piecewise_cron_expression = f'{instance.cron_minute} {instance.cron_hour} {instance.cron_day} {instance.cron_month} {instance.cron_weekday}'
    if cron_expression != piecewise_cron_expression:
        if not cron_expression:
            piecewise_cron_length = len(piecewise_cron_expression.strip().split(' '))
            if piecewise_cron_length == 5:
                instance.cron_expression = piecewise_cron_expression
            else:
                instance.cron_expression = '0 * * * *'
        else:
            split_cron_expression = cron_expression.split(' ')
            if len(split_cron_expression) == 5:
                instance.cron_minute = split_cron_expression[0]
                instance.cron_hour = split_cron_expression[1]
                instance.cron_day = split_cron_expression[2]
                instance.cron_month = split_cron_expression[3]
                instance.cron_weekday = split_cron_expression[4]
            else:
                instance.cron_expression = '0 * * * *'
        tz = pytz.timezone(instance.timezone)
        local_time = datetime.now(tz)
        iter = croniter(instance.cron_expression, local_time)
        instance.next_run = iter.get_next(datetime).astimezone(pytz.utc)
        instance.save()
