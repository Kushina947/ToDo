from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Assignment
from lecture.models import Course
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import AssignmentForm
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

class AssignmentCreateView(LoginRequiredMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignment/assignment_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'course': get_object_or_404(Course, code=self.kwargs.get('code'))}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, code=self.kwargs.get('code'))
        return context


    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.object = form.save()
        from accounts.models import User_Assignment
        User_Assignment.objects.create(user=self.request.user, assignment=self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lecture:lecture', kwargs={'pk': self.kwargs.get('code')})

    def get_initial(self):
        initial = super().get_initial()
        code = self.kwargs.get('code')
        course = get_object_or_404(Course, code=code)
        initial['course'] = course
        return initial


class AssignmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignment/assignment_form.html'


    def get_success_url(self):
        return reverse_lazy('lecture:lecture', kwargs={'pk': self.object.course.code})


class AssignmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Assignment


    def get_success_url(self):
        return reverse_lazy('lecture:lecture', kwargs={'pk': self.object.course.code})


class AssignmentDetailView(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = 'assignment/assignment_detail.html'
    context_object_name = 'assignment'