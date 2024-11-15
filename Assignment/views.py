from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Assignment
from lecture.models import Course
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import AssignmentForm
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from accounts.models import User_Assignment
from lecture.form import CheckForm


class AssignmentCreateView(LoginRequiredMixin, CreateView):
    """
    課題作成ページ
    """
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
        User_Assignment.objects.create(user=self.request.user, assignment=self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lecture:lecture', kwargs={'pk': self.kwargs.get('code')})


class AssignmentUpdateView(LoginRequiredMixin, UpdateView):
    """
    課題編集ページ
    UpdateViewを継承して、課題編集ページをカスタマイズ
    """
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignment/assignment_create.html'

    def get_success_url(self):
        return reverse_lazy('lecture:lecture', kwargs={'pk': self.object.course.code})


class AssignmentDeleteView(LoginRequiredMixin, DeleteView):
    """
    課題削除ページ
    DeleteViewを継承して、課題削除ページをカスタマイズ
    """
    model = Assignment
    template_name = 'assignment/assignment_delete.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('lecture:lecture', kwargs={'pk': self.object.course.code})



class AssignmentDetailView(LoginRequiredMixin, DetailView):
    """
    課題詳細ページ
    DetailViewを継承して、課題詳細ページをカスタマイズ
    """
    model = Assignment
    template_name = 'assignment/assignment_detail.html'
    context_object_name = 'assignment'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = CheckForm()
        # 課題の提出状況を取得
        user_assignment_list = User_Assignment.objects.filter(user=self.request.user)
        user_assignment = []
        for i in user_assignment_list:
            user_assignment.append(i.assignment)
        ctx['user_assignment_list'] = user_assignment #　ユーザーに紐づく課題のリスト ユーザーがその課題を登録しているかどうかの確認に使う
        if User_Assignment.objects.filter(user=self.request.user, assignment=self.object).exists():
            """
            ログイン中のユーザーが課題を登録している場合としていない場合で表示を変えたいのでされていないときはNoneを返す
            具体的な表示はテンプレート側で行う
            """
            ctx['user_assignment'] = User_Assignment.objects.get(user=self.request.user, assignment=self.object)
        else:
            ctx['user_assignment'] = None
        return ctx

    def post(self, request, *args, **kwargs):
        """
        登録するボタンと提出するボタンの処理を分ける
        messageはデバック用
        """
        if request.POST['next'] == 'submit':
            self.object = self.get_object()
            message = ''
            form = CheckForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data['user']
                assignment = form.cleaned_data['assignment']
                try: #登録済みであれば未登録に、未登録であれば登録する
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
        elif request.POST['next'] == 'finish':
            self.object = self.get_object()
            message = ''
            form = CheckForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data['user']
                assignment = form.cleaned_data['assignment']
                try: # 提出済みであれば未提出に、未提出であれば提出済みに更新する
                    if User_Assignment.objects.get(user=user, assignment=assignment).is_finished == 1:
                        User_Assignment.objects.filter(user=user, assignment=assignment).update(is_finished=0)
                    else:
                        User_Assignment.objects.filter(user=user, assignment=assignment).update(is_finished=1)
                except:
                    message = 'エラーが発生しました'
            else:
                message = '入力内容が正しくありません'
            ctx = self.get_context_data()
            ctx['message'] = message
            return self.render_to_response(ctx)

