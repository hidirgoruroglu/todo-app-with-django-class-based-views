from django.shortcuts import render,redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy

from .models import Task

# Create your views here.

class CustomLoginView(LoginView):
    template_name = "todo/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("task_list_view")

class RegisterView(FormView):
    template_name = "todo/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("task_list_view")

    def form_valid(self,form):
        user = form.save()

        if user is not None:
            login(self.request,user)
        return super(RegisterView, self).form_valid(form)
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect("task_list_view")
        return super(RegisterView,self).get(*args,**kwargs)


class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user = self.request.user)
        context["count"] = context["tasks"].filter(complate = False).count()
        
        search_input = self.request.GET.get("search-area") or ""
        if search_input:
            context["tasks"] = context["tasks"].filter(title__startswith = search_input)
        context["search_input"] = search_input
        return context

class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = "task"
    # template_name = "todo/task.html"

class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    fields = ["title","description","complate"]
    success_url = reverse_lazy("task_list_view")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)
    
    

class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ["title","description","complate"]
    success_url = reverse_lazy("task_list_view")

class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("task_list_view")

