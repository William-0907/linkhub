from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

INPUT_CLASSES = 'w-full rounded-xl bg-slate-900 border border-slate-800 px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500'


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': INPUT_CLASSES})


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'you@example.com',
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'username',
            'password1': 'Password',
            'password2': 'Confirm password',
        }
        for name, placeholder in placeholders.items():
            if name in self.fields:
                self.fields[name].widget.attrs.update({
                    'class': INPUT_CLASSES,
                    'placeholder': placeholder,
                })


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'accent_color', 'bg_style']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': INPUT_CLASSES + ' resize-none',
                'placeholder': 'Tell the world about yourself...',
                'rows': 3,
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-slate-400 file:mr-4 file:rounded-xl file:border-0 file:bg-slate-800 file:px-4 file:py-2.5 file:text-sm file:font-semibold file:text-slate-200 hover:file:bg-slate-700 cursor-pointer',
            }),
            'accent_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'h-10 w-16 cursor-pointer rounded-lg border border-slate-800 bg-slate-900 p-1',
            }),
            'bg_style': forms.RadioSelect(attrs={
                'class': 'hidden',
            }),
        }


class StyledPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'old_password': 'Current password',
            'new_password1': 'New password',
            'new_password2': 'Confirm new password',
        }
        for name, placeholder in placeholders.items():
            if name in self.fields:
                self.fields[name].widget.attrs.update({
                    'class': INPUT_CLASSES,
                    'placeholder': placeholder,
                })
