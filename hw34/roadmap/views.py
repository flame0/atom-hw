from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.db import models

from .models import Task, Roadmap, Score
from .forms import TaskForm, TaskEditForm, RoadmapForm

from .utils import stats


@login_required(login_url=reverse_lazy('account:login'))
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user == task.roadmap.user:
        return render(request, 'roadmap/task.html', {'task': task})
    else:
        raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def task_new(request, pk):
    action = 'New'
    roadmap = get_object_or_404(Roadmap, pk=pk)
    if request.user == roadmap.user:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.roadmap = roadmap
                task.save()
                return redirect('roadmap:task', pk=task.pk)
        else:
            form = TaskForm()
        return render(request, 'roadmap/task_edit.html', {'form': form, 'action': action})
    raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def task_update(request, pk):
    import ipdb; ipdb.set_trace()
    task = get_object_or_404(Task, pk=pk)
    action = 'Update'
    if request.user == task.roadmap.user:
        if request.method == 'POST':
            form = TaskEditForm(request.POST, instance=task)
            if form.is_valid():
                task = form.save(commit=False)
                if task.state == 'ready':
                    task.set_score()
                else:
                    task.unset_score()
                task.save()
                return redirect('roadmap:task', pk=task.pk)
        else:
            form = TaskEditForm(instance=task)
        return render(request, 'roadmap/task_edit.html', {'form': form, 'action': action})
    raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    roadmap_pk = task.roadmap.pk
    if request.user == task.roadmap.user:
        task.delete()
        return redirect('roadmap:roadmap', pk=roadmap_pk)
    raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def roadmaps_show(request):
    user = request.user
    roadmaps = user.roadmap_set.all()
    return render(request, 'roadmap/roadmaps.html', {'roadmaps': roadmaps})


@login_required(login_url=reverse_lazy('account:login'))
def roadmap_detail(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk)
    if roadmap.user == request.user:
        tasks = Task.objects.filter(roadmap=roadmap).order_by('state', 'estimate')
        return render(request, 'roadmap/roadmap_detail.html', {'roadmap': roadmap, 'tasks': tasks})
    raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def roadmap_stats(request):
    user = request.user
    roadmaps = user.roadmap_set.all()
    stat_dict = stats(roadmaps)

    sum_score = 0
    for roadmap in roadmaps:
        scores = Score.objects.filter(task__roadmap=roadmap)
        points_earned = scores.aggregate(models.Sum('points'))['points__sum']
        if points_earned is None:
            points_earned = 0
        sum_score += points_earned

    sum_tasks = 0
    for roadmap in roadmaps:
        tasks = Task.objects.filter(roadmap=roadmap).count()
        sum_tasks += tasks
    return render(request, 'roadmap/stat.html', {'weeks': stat_dict['weeks'], 'months': stat_dict['months'],
                                                 'sum_score': sum_score, 'sum_tasks': sum_tasks})


@login_required(login_url=reverse_lazy('account:login'))
def roadmap_new(request):
    if request.method == 'POST':
        form = RoadmapForm(request.POST)
        if form.is_valid():
            roadmap = form.save(commit=False)
            roadmap.user = request.user
            roadmap.save()
            return redirect('roadmap:roadmaps')
    else:
        form = RoadmapForm()
    return render(request, 'roadmap/roadmap_new.html', {'form': form})


@login_required(login_url=reverse_lazy('account:login'))
def roadmap_delete(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk)
    if roadmap.user == request.user:
        roadmap.delete()
    else:
        raise PermissionDenied
    return redirect('roadmap:roadmaps')
