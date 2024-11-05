from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__' 
    term = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    teacher = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    lecture_schedule = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


    def clean_code(self):
        code = self.cleaned_data['code']
        if len(code) > 10:  #
            raise forms.ValidationError("コードは10文字以内で入力してください。")
        return code