from django import forms
from .models import Course
from accounts.models import CustomUser
from assignment.models import Assignment

class CheckForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        empty_label=None,
        label='ユーザー'
    )
    assignment = forms.ModelChoiceField(
        queryset=Assignment.objects.all(),
        empty_label=None,
        label='課題'
    )