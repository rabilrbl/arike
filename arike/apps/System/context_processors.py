from django.urls import reverse


def index_vars(request):
    return {
        "title": "Arike",
        "navitems": {
            "Home": "/",
            "Facility": reverse("facility:index"),
            "Agenda": "#",
            "Patient": "#",
        },
        
        }