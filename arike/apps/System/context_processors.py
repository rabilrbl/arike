from django.urls import reverse


def index_vars(request):
    data = {
        "title": "Arike",
        "navitems": {
            "Home": "/",
            "Users": reverse("distadmin:users"),
            "Facility": reverse("facility:index"),
            "Agenda": "#",
            "Patient": reverse("patient:patients"),
        },
        
        }
    if request.user.is_authenticated:
        data["navitems"]['Profile'] = reverse('users:update')
    return data