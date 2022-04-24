from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView, UpdateView

from .models import News


class MainView(TemplateView):
    template_name = 'news_main.html'

    def get(self, request):
        if request.user.is_authenticated:
            news = News.objects.filter(author=request.user)
            ctx = {'news': news}
            return render(request, self.template_name, ctx)
        else:
            return render(request, self.template_name, {})


class LoginView(FormView):
    form_class = AuthenticationForm
    success_url = '/news/'
    template_name = 'login.html'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        return super(LoginView, self).form_valid(form)

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/news/')

class AddNewsView(CreateView):
    fields = ['title', 'content', 'tags', 'category']
    model = News
    success_url = '/news/'
    template_name = 'add_edit_news.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        for tag in form.cleaned_data['tags']:
            self.object.tags.add(tag.id)
        self.object.save()
        return redirect(self.success_url)

class EditNewsView(UpdateView):
    model = News
    success_url ='/news/'
    template_name = 'add_edit_news.html'

    fields = ['title', 'content', 'tags', 'category']

    def get_object(self, queryset=None):
        obj = News.objects.get(id=self.kwargs['pk'])
        return obj


