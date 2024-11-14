from django import forms
from .models import Assignment
from lecture.models import Course
import datetime

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
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label=None)

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['deadline'].initial = datetime.datetime.now().strftime('%Y-%m-%dT23:59')
