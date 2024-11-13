from django import forms

class CommentForm(forms.Form):
    content = forms.CharField(max_length=100, label='')