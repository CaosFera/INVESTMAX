





import os
from celery import Celery
from celery.schedules import timedelta
from celery.schedules import crontab 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investmax.settings')

app = Celery('investmax')

# Carregar configurações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Configurações do broker e backend
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

# Configurações do Beat
app.conf.beat_schedule = {
    "every-minute-task": {
        "task": "investments.tasks.update_all_investments",
        "schedule": crontab(minute='*/1'),
    }
}

# Descobre as tarefas em apps Django
app.autodiscover_tasks()
broker_connection_retry_on_startup = True