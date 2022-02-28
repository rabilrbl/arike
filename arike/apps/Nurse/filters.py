from django_filters import FilterSet, OrderingFilter
from arike.apps.Patient.models import VisitSchedule, Treatment, Patient


INPUTCLASS = "textinput w-full rounded-lg block bg-white text-gray-700 focus:outline-none appearance-none leading-normal py-2 border px-4 border-gray-300 mb-2"

class TreatmentFilter(FilterSet):
    sort = OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ),
        field_labels={
            'created_at': 'Date creation',
            'updated_at': 'Last updated',
        },
        label='Sort by'
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for s in self.filters:
            self.filters[s].field.widget.attrs.update({
                'class': INPUTCLASS,
            })

    class Meta:
        model = VisitSchedule
        fields = ['patient', 'date', 'time', 'duration']



