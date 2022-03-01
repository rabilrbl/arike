from django.urls import reverse


def index_vars(request):
    data = {
        "title": "Arike",
        "navitems": {
            "Home": "/",
        },
        
    }
    if request.user.is_authenticated and request.user.role == 1:
        data["navitems"]['Users'] = reverse("distadmin:users")
        data["navitems"]['Facility'] = reverse("facility:index")
    
    
    data["navitems"]['Agenda'] = reverse("nurse:agenda")
    data["navitems"]['Schedule'] = reverse("nurse:schedule")
    
    data["navitems"]['Patient'] = reverse("patient:patients")
    data["navitems"]['Profile'] = reverse('users:update')
    
    
    return data