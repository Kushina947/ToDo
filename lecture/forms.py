from django import forms
from .models import Course
from accounts.models import CustomUser


class CourseAddForm(forms.Form):
    search_code = forms.CharField(label='開講番号', max_length=10, required=False)
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def search_courses(self, search_code):
        if search_code:
            self.fields['courses'].queryset = Course.objects.filter(code=search_code)
        else:
            self.fields['courses'].queryset = Course.objects.none()