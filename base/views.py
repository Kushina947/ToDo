from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView

class HomeView(TemplateView):
    template_name = "base/home.html"

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        class Task:
            def __init__(self, title, description, due_date=None):
                self.title = title
                self.description = description
                self.due_date = due_date
        task = Task('Home', 'This is the home page.', '2021-01-01')
        ctx['task'] = task
        ctx['user'] = self.request.user

        return ctx
