from django import forms

from .models import Link


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['title', 'url', 'platform']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full rounded-xl bg-slate-900 border border-slate-800 px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Link title',
            }),
            'url': forms.URLInput(attrs={
                'class': 'w-full rounded-xl bg-slate-900 border border-slate-800 px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'https://example.com',
            }),
            'platform': forms.Select(attrs={
                'class': 'w-full rounded-xl bg-slate-900 border border-slate-800 px-4 py-3 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            }),
        }
