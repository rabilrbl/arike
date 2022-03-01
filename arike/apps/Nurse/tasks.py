from datetime import datetime, timedelta
from pytz import timezone
from django.core.mail import send_mail
from arike.apps.Patient.models import VisitSchedule, Treatment
from arike.apps.Nurse.models import Reports
from config  import celery_app
from celery.schedules import crontab


def send_email_report(report) -> None:
    user = report.user
    task = VisitSchedule.objects.filter(user=user, deleted=False, date=datetime.now().date())
    print(f"Sending email reminder to {user.full_name}\n")
    patients = task.count()
    # TODO : add more details   (treatment, note, etc)
    email_content = f"""
        Hi {user.full_name},
        \n\nYou have treated {patients} patients today.
        \n\nRegards,\nArike Team
    """
    send_mail(
        "Arike Daily Report",
        (email_content),
        "arikecare@gmail.com",
        [user.email],
        fail_silently=False,  # Throw exception if email fails to send
    )
    today = datetime.now().date()
    # increment by a day
    report.last_sent = datetime(today.year, today.month, today.day, report.last_sent.hour, report.last_sent.minute, report.last_sent.second, tzinfo=timezone('UTC')) + timedelta(days=1)
    report.save()
    print("Email sent to {}".format(user.email))


@celery_app.task
def periodic_emailer():
    currentTime = datetime.now(timezone('UTC'))
    print("Checking time for user daily report......")
    reports = Reports.objects.filter(
        last_sent__lte=currentTime,
        consent=True
    )
    for rpt in reports:
        send_email_report(rpt)


celery_app.conf.beat_schedule = {
    'send-email-report': {
        'task': 'arike.apps.Nurse.tasks.periodic_emailer',
        'schedule': crontab(minute='*/5'),
    },
}