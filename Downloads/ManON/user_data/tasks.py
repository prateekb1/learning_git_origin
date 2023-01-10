from django.core.mail import send_mail
from celery.utils.log import get_task_logger
from celery import shared_task
from time import sleep
from ManOn_backend import settings

logger = get_task_logger(__name__)


@shared_task(name='my_first_task')
def my_first_task(duration):
    sleep(duration)
    return ("task_done")


@shared_task(name="email_sent")
def email_sent(data):
    subject = 'Reset Your Password'
    message = data["body"]
    receiver = data["email_receiver"]
    is_task_completed = False
    try:
        sleep(data['duration'])
        is_task_completed = True
    except Exception as err:
        error = str(err)
        logger.error(error)
    if is_task_completed:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [receiver, ], fail_silently=False)
    return ('first_task_done')


@shared_task(name="otp_delete")
def otp_delete(data):
    pass
