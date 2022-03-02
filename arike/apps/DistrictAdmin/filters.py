from django.contrib.auth import get_user_model
from django_filters import FilterSet, OrderingFilter

User = get_user_model()

INPUTCLASS = """textinput w-full rounded-lg block bg-white text-gray-700
    focus:outline-none appearance-none leading-normal py-2 border px-4
    border-gray-300 mb-2"""


class UserFilter(FilterSet):
    """
    Filters for the User model
    """
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
        self.filters['full_name'].label = 'Name'
        self.filters['facility'].label = 'Facility'
        self.filters['role'].label = 'Role'
        self.filters['full_name'].field.widget.attrs.update({
            'class': INPUTCLASS,
        })
        self.filters['facility'].field.widget.attrs.update({
            'class': INPUTCLASS,
        })
        self.filters['role'].field.widget.attrs.update({
            'class': INPUTCLASS,
        })
        self.filters['sort'].field.widget.attrs.update({
            'class': INPUTCLASS,
        })
        self.filters['full_name'].lookup_expr = 'icontains'

    class Meta:
        model = User
        fields = ['full_name', 'role', 'facility']
