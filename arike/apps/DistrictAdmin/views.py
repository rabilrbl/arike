
# import GenericViews
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


User = get_user_model()


class UserIndexView(ListView):
    """
    District Admin User list page
    """
    template_name = 'DistrictAdmin/users.html'
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.filter(role__range=(3, 4), deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Users'
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

class NewUser(CreateView):
    form_class = NewUserForm
    template_name = 'DistrictAdmin/new_user.html'
    success_url = reverse_lazy('distadmin:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New User'
        return context
    
class UserDetailView(DetailView):
    """
    District Admin User detail page
    """
    model = User
    template_name = 'DistrictAdmin/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User Detail'
        return context


class UserUpdateView(UpdateView):
    """
    District Admin User update page
    """
    model = User
    form_class = NewUserForm
    template_name = 'DistrictAdmin/user_update.html'
    success_url = reverse_lazy('DistrictAdmin:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update User'
        return context


class UserDeleteView(DeleteView):
    """
    District Admin User delete page
    """
    model = User
    template_name = 'DistrictAdmin/user_delete.html'
    success_url = reverse_lazy('distadmin:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete User'
        return context
