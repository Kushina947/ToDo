from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import CustomUser
from django.core.exceptions import ValidationError


class CustomAuthenticationForm(AuthenticationForm):
     def __init__(self, *args, **kwargs):
         kwargs.setdefault('label_suffix', '')
         super().__init__(*args, **kwargs)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser