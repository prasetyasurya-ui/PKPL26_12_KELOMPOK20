from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


FIELD_CLASS = (
    'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm '
    'text-slate-800 outline-none transition placeholder:text-slate-400 '
    'focus:border-brand-500 focus:ring-4 focus:ring-brand-100'
)


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': FIELD_CLASS})


class ECommerceRegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        label='Peran Pengguna',
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': FIELD_CLASS})
