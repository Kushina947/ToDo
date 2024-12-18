from .form import CustomAuthenticationForm, CustomUserCreationForm
from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser

class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = CustomAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('base:home')
        return super().dispatch(request, *args, **kwargs)

class SignUpView(FormView):
    template_name = "registration/sign_up.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        if self.request.POST['next'] == 'back':
            return render(self.request, 'registration/sign_up.html', {'form': form})
        elif self.request.POST['next'] == 'confirm':
            form.pass_confirm = f'{form.cleaned_data["password1"][0]}'
            for i in range(2, len(form.cleaned_data['password1'])):
                form.pass_confirm += '*'
            form.pass_confirm += f'{form.cleaned_data["password1"][-1]}'
            return render(self.request, 'registration/sign_up_confirm.html', {'form': form})
        elif self.request.POST['next'] == 'register':
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(self.request, user)
            return super().form_valid(form)
        else:
            return redirect(reverse_lazy('base:home'))

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('base:home')
        return super().dispatch(request, *args, **kwargs)

class CustomLogoutView(LogoutView):
    template_name = "registration/logged_out.html"

class ProfileView(TemplateView):
    template_name = "registration/profile.html"

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        ctx['user'] = self.request.user
        return ctx

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['username', 'email', 'icon']
    template_name = 'registration/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.instance.icon = self.request.FILES.get('icon', form.instance.icon)
        return super().form_valid(form)


