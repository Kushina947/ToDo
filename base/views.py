from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from accounts.models import CustomUser, User_Assignment
from assignment.models import Assignment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import ModelFormMixin
from base.form import CourseSearchForm
from lecture.models import Course
from lecture.form import CheckForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "base/home.html"

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        ctx['user_assignments'] = User_Assignment.objects.filter(user=self.request.user)
        course_list = CustomUser.objects.get(id=self.request.user.id).courses.all()
        for course in course_list:
            course.assignment_count = Assignment.objects.filter(course=course).count()
            course.assignment_count -= User_Assignment.objects.filter(user=self.request.user, assignment__course=course).count()
        ctx['courses'] = course_list
        ctx['form'] = CourseSearchForm()
        return ctx

    def post(self, request, *args, **kwargs):
        if request.POST['next'] == 'submit':
            form = CourseSearchForm(request.POST)
            if form.is_valid():
                search_code = form.cleaned_data['course_code']
                try:
                    if request.user.courses.filter(code=search_code).exists():
                        message = f'{search_code} はすでに追加されています'
                    else:
                        course = Course.objects.get(code=search_code)
                        request.user.courses.add(course)
                        message = f'{course.name} を追加しました'
                except Course.DoesNotExist:
                    message = f'{search_code} は存在しません'
            else:
                message = '入力内容が正しくありません'

            ctx = self.get_context_data()
            ctx['message'] = message
            return self.render_to_response(ctx)
        elif request.POST['next'] == 'finish':
            message = ''
            form = CheckForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data['user']
                assignment = form.cleaned_data['assignment']
                try:
                    if User_Assignment.objects.get(user=user, assignment=assignment).is_finished == 1:
                        User_Assignment.objects.filter(user=user, assignment=assignment).update(is_finished= 0)
                    else:
                        User_Assignment.objects.filter(user=user, assignment=assignment).update(is_finished= 1)
                except:
                    message = 'エラーが発生しました'
            else:
                message = '入力内容が正しくありません'
            ctx = self.get_context_data()
            ctx['message'] = message
            return self.render_to_response(ctx)


