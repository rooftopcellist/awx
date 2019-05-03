import random
import logging

from django.db import migrations, models
from django.utils.timezone import now, timedelta

logger = logging.getLogger('awx.main.migrations')

__all__ = ['create_system_job_templates']

def create_system_job_templates(apps, schema_editor):
    '''
    Create default system job templates if not present. Create default schedules
    only if new system job templates were created (i.e. new database).
    '''

    SystemJobTemplate = apps.get_model('main', 'SystemJobTemplate')
    Schedule = apps.get_model('main', 'Schedule')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    sjt_ct = ContentType.objects.get_for_model(SystemJobTemplate)
    now_dt = now()
    random_time = now() + timedelta(minutes=random.randint(-30,30))
    random_schedule_time = random_time.strftime('%Y%m%dT%H%M%SZ')

    sjt, created = SystemJobTemplate.objects.get_or_create(
        job_type='gather_analytics --ship',
        defaults=dict(
            name='Automation Insights Collection',
            description='Collect analytics data and send it to Automation Insights',
            created=now_dt,
            modified=now_dt,
            polymorphic_ctype=sjt_ct,
        ),
    )
    if created:
        sched = Schedule(
            name='Gather Automation Insights',
            rrule='DTSTART:%s RRULE:FREQ=DAILY;INTERVAL=1;COUNT=1' % random_schedule_time,
            description='Automatically Generated Schedule',
            enabled=False,
            extra_data={},
            created=now_dt,
            modified=now_dt,
        )
        sched.unified_job_template = sjt
        sched.save()
