from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import Course
from .form import CheckForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from assignment.models import Assignment
from thread.models import Post
from accounts.models import User_Assignment


class LectureView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "lecture/lecture.html"
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        ctx = super().get_context_data(**kwargs)
        ctx['assignments'] = Assignment.objects.filter(course=self.object)
        thread_list = Post.objects.filter(course=self.object)
        for thread in thread_list:
            last_comment = thread.comment_set.order_by('-created_at').first()
            if last_comment is not None:
                thread.last_update = last_comment.created_at
            else:
                thread.last_update = thread.created_at
        thread_list = sorted(thread_list, key=lambda x: x.last_update, reverse=True)
        ctx['threads'] = thread_list
        user_assignment_list = User_Assignment.objects.filter(user=self.request.user)
        user_assignment = []
        for i in user_assignment_list:
            user_assignment.append(i.assignment)
        ctx['user_assignments'] = user_assignment
        ctx['form'] = CheckForm()
        ctx['is_finished_form'] = CheckForm()
        return ctx
    
    def post(self, request, *args, **kwargs):
        message = ''
        form = CheckForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            assignment = form.cleaned_data['assignment']
            try:
                if User_Assignment.objects.filter(user=user, assignment=assignment).exists():
                    User_Assignment.objects.filter(user=user, assignment=assignment).delete()
                else:
                    User_Assignment.objects.create(user=user, assignment=assignment)
            except:
                message = 'エラーが発生しました'
        else:
            message = '入力内容が正しくありません'

        ctx = self.get_context_data()
        ctx['message'] = message
        return self.render_to_response(ctx)