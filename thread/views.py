from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from thread.models import Post, Comment


class ThreadView(DetailView):
    template_name = "thread/thread.html"
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = Comment.objects.filter(post=self.object)
        ctx['comments'] = ctx['comments'].order_by('created_at')
        return ctx