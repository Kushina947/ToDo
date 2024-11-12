from django import forms

class CourseSearchForm(forms.Form):
    course_code = forms.CharField(max_length=10, label='開講番号')