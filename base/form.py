from django import forms

class CourseSearchForm(forms.Form):
    course_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder': '開講番号を入力'}),
        label=''
    )