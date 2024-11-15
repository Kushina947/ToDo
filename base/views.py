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
        user_assignment = User_Assignment.objects.filter(user=self.request.user)
        # 課題の締め切り近いものが上に表示されるようにソート
        sorted_user_assignment = sorted(user_assignment, key=lambda x: x.assignment.deadline)
        ctx['user_assignments'] = sorted_user_assignment
        course_list = CustomUser.objects.get(id=self.request.user.id).courses.all()
        for course in course_list: # 講義に登録されている課題の中で登録していないものをカウント
            course.assignment_count = Assignment.objects.filter(course=course).count()
            course.assignment_count -= User_Assignment.objects.filter(user=self.request.user, assignment__course=course).count()
        ctx['courses'] = course_list
        ctx['form'] = CourseSearchForm()
        return ctx

    def post(self, request, *args, **kwargs):
        if request.POST['next'] == 'submit':
            # 講義の追加
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
            # 課題の提出状況を変更
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


