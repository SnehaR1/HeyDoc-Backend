from celery import shared_task
from django.core.mail import EmailMessage
from time import sleep
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, name="send_email_task")
def send_mail_task(
    self,
    subject,
    message,
    email_from,
    recepient_list,
):
    try:
        send_mail(subject, message, email_from, recepient_list, fail_silently=True)
        logger.info("Mail sent successfully")
    except Exception as e:
        logger.error(f"Mail sending failed: {str(e)}")


# celery -A HeyDoc worker -l info -P gevent
