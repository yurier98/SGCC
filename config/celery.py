import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.develop')

# Get the base REDIS URL, default to redis' default
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

app = Celery('GEPRE')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


from celery.schedules import crontab

# app.conf.beat_schedule = {
#     'eliminar-registros-antiguos-cada-tres-meses': {
#         'task': 'apps.audit.tasks.eliminar_registros_antiguos',
#         'schedule': crontab(minute=0, hour=0, day_of_month='1', month_of_year='*/3'),
#     },
# }

app.conf.beat_schedule = {
    'eliminar-registros-antiguos-cada-tres-meses': {
        'task': 'apps.audit.tasks.eliminar_registros_antiguos',
        'schedule': crontab(minute=0, hour=9, day_of_month='1', month_of_year='*/3'),
    },
}



