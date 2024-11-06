from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomAuthenticationForm(AuthenticationForm):
     def __init__(self, *args, **kwargs):
         kwargs.setdefault('label_suffix', '')
         super().__init__(*args, **kwargs)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
