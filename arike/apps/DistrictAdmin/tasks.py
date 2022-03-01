from config import celery_app
from django.core.mail import send_mail


@celery_app.task(retry_backoff=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def send_email(subject, message, from_email, recipient_list, fail_silently=False, html_message=None):
    """
    Send email using celery
    """
    send_mail(subject, message, from_email, recipient_list, fail_silently=fail_silently, html_message=html_message)