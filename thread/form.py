from django import forms
from .models import Post
from lecture.models import Course

class CommentForm(forms.Form):
    content = forms.CharField(max_length=100, label='')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'course']
        labels = {
            'title': 'タイトル',
            'content': '内容',
            'course': '科目名',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label=None)