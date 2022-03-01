from django_filters import FilterSet, OrderingFilter

from arike.apps.DistrictAdmin.filters import INPUTCLASS
from arike.apps.Patient.models import Patient


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
        model = Patient
        fields = ['full_name']
