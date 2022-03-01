
from django.core.mail import send_mass_mail

from config import celery_app


@celery_app.task(retry_backoff=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def send_report_to_family_members(instance, family,**kwargs):
    visitdata = instance
    subject = 'Patient Visit Report from Arike'
    message = f'''Dear Family member,
This is your patient {visitdata['full_name']} visit report.\n
Palliative Phase: 
    {visitdata['palliative_phase']}\n
Blood Pressure: 
    {visitdata['blood_pressure']}\n
Pulse Rate: {visitdata['pulse']}\n
General Random Blood Pressure: {visitdata['general_random_blood_pressure']}\n
Patient at Peace: {visitdata['patient_at_peace']}\n
Public Hygiene: 
    {visitdata['public_hygiene']}\n
Personal Hygiene:
    {visitdata['personal_hygiene']}\n
Mouth Hygiene: 
    {visitdata['mouth_hygiene']}\n
Systemic Examination: 
    {visitdata['systemic_examination']}\n
Note: 
    {visitdata['note']}\n
Thank you,
    Arike'''
    message = ((subject, message, 'arikecare@gmail.com', [fam['email']]) for fam in family)
    return send_mass_mail(message, fail_silently=False)
