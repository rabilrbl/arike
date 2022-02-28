from django.template import Library
from arike.apps.Patient.models import Treatment
from arike.apps.System.models import Ward
from django.contrib.auth import get_user_model

User = get_user_model()

register = Library()

@register.simple_tag(takes_context=True)
def treatment(context, patient):
    context['treatments'] = Treatment.objects.filter(patient=patient)
    return ''
    