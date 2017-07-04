from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView

from todo.forms import CreateTaskForm, EditTaskForm, LoginForm
from todo.models import Task


class Login(View):
    template_name = 'todo/login.html'

    def get(self, request):
        remember_me = request.COOKIES.get('username') or None
        form = LoginForm()

        if remember_me:
            data = {'username': remember_me, 'remember_me': True}
            form = LoginForm(data)

        return render(request, Login.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)

        user = authenticate(username=username, password=password)

        if not user:
            messages.error(request, 'Username/Password is incorrect. Please try again.')
            return HttpResponseRedirect(reverse('todo:login'))

        login(request, user)
        request.session['task_count'] = 0
        response = HttpResponseRedirect(reverse('todo:home'))
        saved_username = request.COOKIES.get('username', False)

        if remember_me:
            response.set_cookie('username', username, max_age=86400)
        elif not remember_me and saved_username:
            response.delete_cookie('username')

        return response


class Home(View):
    template_name = 'todo/list.html'

    def get(self, request):
        form = CreateTaskForm()
        tasks = Task.objects.filter(user=request.user)
        page = request.GET.get('page') or None
        paginator = Paginator(tasks, 4)
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            tasks = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            tasks = paginator.page(paginator.num_pages)

        tasks_count = Task.objects.filter(user=request.user).count()
        tasks_done = Task.objects.filter(user=request.user, done=True).count()

        return render(request, Home.template_name, {'tasks': tasks,
                                                    'form': form,
                                                    'tasks_count': tasks_count,
                                                    'tasks_done': tasks_done})

    def post(self, request):
        tasks = Task.objects.filter(user=request.user)
        page = request.GET.get('page')
        paginator = Paginator(tasks, 4)
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)

        tasks_count = Task.objects.filter(user=request.user).count()
        tasks_done = Task.objects.filter(user=request.user, done=True).count()

        if request.session.get('task_count') == 5:
            messages.error(request, 'You reached your limit of 5 tasks per session.')
            return redirect('todo:home')

        form = CreateTaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            request.session['task_count'] += 1
            return HttpResponseRedirect(reverse('todo:home'))

        return render(request, Home.template_name, {'tasks': tasks,
                                                    'form': form,
                                                    'tasks_count': tasks_count,
                                                    'tasks_done': tasks_done})


class TaskEdit(UpdateView):
    model = Task
    form_class = EditTaskForm
    template_name = 'todo/task_form.html'
    success_url = reverse_lazy('todo:home')


def delete(request, pk):
    page = request.GET.get('page')
    task = get_object_or_404(Task, id=pk)
    task.delete()

    response = redirect(reverse('todo:home'))
    response['Location'] += '?page={}'.format(page)
    return response


def done(request, pk):
    task = get_object_or_404(Task, id=pk)
    task.done = True
    task.save()

    return redirect(reverse('todo:home'))


def login_redirect(request):
    return redirect(reverse('todo:login'))
