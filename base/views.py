from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from accounts.models import CustomUser, User_Assignment
from assignment.models import Assignment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import ModelFormMixin
from base.form import CourseSearchForm
from lecture.models import Course


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "base/home.html"

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        ctx['user_assignments'] = User_Assignment.objects.filter(user=self.request.user)
        ctx['courses'] = CustomUser.objects.get(id=self.request.user.id).courses.all()
        ctx['form'] = CourseSearchForm()
        return ctx

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        form = CourseSearchForm(request.POST)
        if form.is_valid():
            search_code = form.cleaned_data['course_code']
            try:
                course = Course.objects.get(code=search_code)
                request.user.courses.add(course)
                ctx['message'] = f'{course.name} を追加しました'
            except Course.DoesNotExist:
                ctx['message'] = f'{search_code} は存在しません'
        else:
            ctx['message'] = '入力内容が正しくありません'
        return self.render_to_response(ctx)

