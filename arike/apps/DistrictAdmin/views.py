
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import ModelForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from arike.apps.DistrictAdmin.filters import UserFilter
from django.contrib.auth.mixins import PermissionRequiredMixin
from allauth.utils import build_absolute_uri
from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
from allauth.account.utils import user_pk_to_url_str
from django.contrib import messages
from arike.apps.DistrictAdmin.tasks import send_email
from django.contrib.messages.views import SuccessMessageMixin


User = get_user_model()


class UserIndexView(PermissionRequiredMixin ,ListView):
    """
    District Admin User list page
    """
    template_name = 'DistrictAdmin/users.html'
    context_object_name = "users"

    permission_required = 'users.view_user'

    def filter_queryset(self, queryset):
        self.myFilter = UserFilter(self.request.GET, queryset=queryset)
        return self.myFilter.qs

    def get_queryset(self):
        queryset = User.objects.filter(district=self.request.user.district, role__range=(3,4))
        queryset = self.filter_queryset(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Users'
        context['sfield'] = "full_name"
        context['myfilter'] = self.myFilter
        return context

class NewUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        className = "px-4 py-2 rounded-xl border border-gray-400 focus:outline-none focus:border-gray-500"
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({
            "class": className,
        })
        self.fields['email'].widget.attrs.update({
            "class":className, 'required':'true'
        }),
        self.fields['facility'].widget.attrs.update({
            "class":className, 'required':'true'
        })
        self.fields['role'].widget.attrs.update({
            "class":className, 'required':'true'
        })

    class Meta:
        model = User
        fields = ['full_name','email','facility','role']

class NewUser(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = NewUserForm
    template_name = 'DistrictAdmin/new_user.html'
    success_url = reverse_lazy('distadmin:users')

    permission_required = 'users.add_user'

    success_message = 'User was successfully created, an email will be sent to the user!'

    # send email confirmation on user is created
    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            # send the password set email
            token_generator = EmailAwarePasswordResetTokenGenerator()
            temp_key = token_generator.make_token(user)
            path = reverse(
                "account_reset_password_from_key",
                kwargs=dict(uidb36=user_pk_to_url_str(user), key=temp_key),
            )
            url = build_absolute_uri(self.request, path)
            send_email.delay(
                subject=f'Welcome to Arike {user.full_name}',
                message=f'''Please click on the link below to set your password \n
{url}\n\n We are happy to have you on board!\n
You were added by the District Admin {self.request.user.full_name}.
If you are not {user.full_name} please contact us Immediately.
\n\n Thank you! \n Arike Team''',
                from_email= "arikecare@gmail.com",
                recipient_list=[user.email],
                fail_silently=False,
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New User'
        return context
    
class UserDetailView(PermissionRequiredMixin ,DetailView):
    """
    District Admin User detail page
    """
    model = User
    template_name = 'DistrictAdmin/user_detail.html'

    permission_required = 'users.view_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User Detail'
        return context


class UserUpdateView(PermissionRequiredMixin ,UpdateView):
    """
    District Admin User update page
    """
    model = User
    form_class = NewUserForm
    template_name = 'DistrictAdmin/user_update.html'
    success_url = reverse_lazy('distadmin:users')

    permission_required = 'users.change_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update User'
        return context


class UserDeleteView(PermissionRequiredMixin ,DeleteView):
    """
    District Admin User delete page
    """
    model = User
    template_name = 'DistrictAdmin/user_delete.html'
    success_url = reverse_lazy('distadmin:users')

    permission_required = 'users.delete_user'

    def form_valid(self, form):
        if form.is_valid():
            messages.success(self.request, 'User Successfully Deleted')
            return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete User'
        return context
