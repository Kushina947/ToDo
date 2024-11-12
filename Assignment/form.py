from django import forms
from .models import Assignment
from lecture.models import Course

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'deadline', 'description']
        labels = {
            'course': '科目名',
            'title': 'タイトル',
            'deadline': '提出期限',
            'description': '見出し',
        }
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label=None)