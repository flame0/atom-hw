from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.db import models

from account.models import Account
from .models import Task, Roadmap, Score
from .forms import TaskForm, TaskEditForm, RoadmapForm

from datetime import date, datetime, timedelta
from calendar import monthrange
from .utilities import monday_of_week_one


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
                task = form.save(commit=False)
                if task.state == 'ready':
                    task.set_score()
                else:
                    task.unset_score()
                task.save()
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
def roadmap_stats(request):
    account = request.user.account
    roadmaps = account.roadmap_set.all()

    weeks = []
    cur_month = datetime.now().month
    cur_year = datetime.now().year
    init_date = monday_of_week_one(cur_year)
    for i in range(0, 52):
        from_date = init_date
        to_date = init_date + timedelta(days=6)
        title = from_date.strftime("%Y-%m-%d") + ' / ' + to_date.strftime("%Y-%m-%d")
        weeks.append({'from_date': from_date,
                    'to_date':     to_date,
                    'tasks_completed': 0,
                    'tasks_created':   0,
                    'title': title,
                    'number': i+1})
        init_date = init_date + timedelta(days=7)
    for roadmap in roadmaps:
        for week in weeks:
            tasks_created = roadmap.task_set.filter(created__range=(week['from_date'], week['to_date']))
            tasks_completed = roadmap.task_set.filter(score__date__range=(week['from_date'], week['to_date']))
            week['tasks_created'] += tasks_created.count()
            week['tasks_completed'] += tasks_completed.count()

    months = []
    init_date = monday_of_week_one(datetime.now().year)
    for i in range(1,13):
        from_date = datetime(cur_year, i, 1)
        to_date = datetime(cur_year, i, monthrange(cur_year, i)[1])
        months.append({ 'from_date': from_date,
                        'to_date':   to_date,
                        'title':     from_date.strftime("%Y-%m"),
                        'points_earned': 0})

    for roadmap in roadmaps:
        for month in months:
            scores = Score.objects.filter(task__roadmap=roadmap, date__range=(month['from_date'], month['to_date']))
            points_earned = scores.aggregate(models.Sum('points'))['points__sum']
            if points_earned is None:
                points_earned = 0
            month['points_earned'] += points_earned

    return render(request, 'roadmap_stat.html', {'weeks': weeks, 'months': months})



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