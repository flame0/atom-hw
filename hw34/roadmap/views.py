from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

from account.models import Account
from .models import Task, Roadmap
from .forms import TaskForm, TaskEditForm, RoadmapForm


@login_required(login_url=reverse_lazy('account:login'))
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user.account == task.roadmap.account:
        return render(request, 'task.html', {'task': task})
    else:
        raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def task_new(request, pk):
    action = 'New'
    roadmap = get_object_or_404(Roadmap, pk=pk)
    if request.user.account == roadmap.account:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.roadmap = roadmap
                task.save()
                return redirect('roadmap:task', pk = task.pk)
        else:
            form = TaskForm()
        return render(request, 'task_edit.html', {'form': form, 'action': action})
    raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    action = 'Update'
    if request.user.account == task.roadmap.account:
        if request.method == 'POST':
            form = TaskEditForm(request.POST, instance=task)
            if form.is_valid():
                task = form.save()
                #msg = 'Task has been edited'
                return redirect('roadmap:task', pk=task.pk)
        else:
            form = TaskEditForm(instance=task)
        return render(request, 'task_edit.html', {'form': form, 'action': action})
    raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    roadmap_pk = task.roadmap.pk
    if request.user.account == task.roadmap.account:
        task.delete()
        return redirect('roadmap:roadmap', pk=roadmap_pk)
    raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def roadmaps_show(request):
    account = request.user.account
    roadmaps = account.roadmap_set.all()
    return render(request, 'roadmaps.html', {'roadmaps': roadmaps})


@login_required(login_url=reverse_lazy('account:login'))
def roadmap_detail(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk)
    if roadmap.account == request.user.account:
        tasks = Task.objects.filter(roadmap=roadmap).order_by('state', 'estimate')
        return render(request, 'roadmap_detail.html', {'roadmap': roadmap, 'tasks': tasks})
    raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def roadmap_new(request):
    if request.method == 'POST':
        form = RoadmapForm(request.POST)
        if form.is_valid():
            roadmap = form.save(commit=False)
            roadmap.account = request.user.account
            roadmap.save()
            return redirect('roadmap:roadmaps')
    else:
        form = RoadmapForm()
    return render(request, 'roadmap_new.html', {'form': form})


@login_required(login_url=reverse_lazy('account:login'))
def roadmap_delete(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk)
    if roadmap.account == request.user.account:
        roadmap.delete()
    else:
         raise PermissionDenied
    return redirect('roadmap:roadmaps')