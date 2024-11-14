from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from thread.models import Post, Comment
from thread.form import CommentForm, PostForm
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from lecture.models import Course
from django.shortcuts import get_object_or_404


class ThreadView(DetailView):
    template_name = "thread/thread.html"
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = Comment.objects.filter(post=self.object)
        ctx['comments'] = ctx['comments'].order_by('created_at')
        ctx['form'] = CommentForm()
        return ctx
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        ctx = self.get_context_data()
        if form.is_valid():
            content = form.cleaned_data['content']
            Comment.objects.create(
                post=self.object,
                user=request.user,
                content=content
            )
            return redirect('thread:thread', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

class ThreadCreateView(LoginRequiredMixin, CreateView):
    template_name = "thread/thread_create.html"
    model = Post
    form_class = PostForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = PostForm()
        ctx['course'] = get_object_or_404(Course, code=self.kwargs.get('code'))
        return ctx

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lecture:lecture', kwargs={'pk': self.kwargs.get('code')})