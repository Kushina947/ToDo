from django.shortcuts import redirect
from .models import Course
from .form import CheckForm, CourseDelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from assignment.models import Assignment
from thread.models import Post
from accounts.models import User_Assignment


class LectureView(LoginRequiredMixin, DetailView):
    """
    講義ページ
    """
    model = Course
    template_name = "lecture/lecture.html"
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        ctx = super().get_context_data(**kwargs)
        assignment = Assignment.objects.filter(course=self.object)
        # 最新の課題から表示されるように　講義ページでは登録ボタンをつけるため、新しい課題が上に来たほうが使いやすそう
        sorted_assignment = sorted(assignment, key=lambda x: x.deadline, reverse=True)
        ctx['assignments'] = sorted_assignment
        thread_list = Post.objects.filter(course=self.object)
        for thread in thread_list: # スレッドの最終更新日時を取得
            last_comment = thread.comment_set.order_by('-created_at').first()
            if last_comment is not None:
                thread.last_update = last_comment.created_at
            else:
                thread.last_update = thread.created_at
        # 最終更新日が近いスレッドから表示されるように
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
        # 自分の課題として登録するボタンの処理
        if request.POST['next'] == 'finish':
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

        elif request.POST['next'] == 'del':
            print('delが実行されました')
            #　講義の登録を解除
            message = ''
            form = CourseDelForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data['user']
                course = form.cleaned_data['course']
                try:
                    user.courses.remove(course)
                    return redirect('base:home')
                except:
                    pass
            else:
                print('else')
                message = '入力内容が正しくありません'
            ctx = self.get_context_data()
            ctx['message'] = message
            return self.render_to_response(ctx)