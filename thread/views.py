from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from thread.models import Post, Comment
from thread.form import CommentForm


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