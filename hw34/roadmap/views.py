from django.shortcuts import render, get_object_or_404, redirect
#from .forms import TaskForm, TaskEditForm, RoadmapForm
from .models import Task, Roadmap
from .forms import TaskForm, TaskEditForm, RoadmapForm
import datetime

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task.html', {'task': task})

def task_new(request, pk):
    action = 'New'
    roadmap = get_object_or_404(Roadmap, pk=pk)
    if request.method =='POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.roadmap = roadmap
            task.save() 
            return redirect('roadmap:task', pk = task.pk)
    else:
        form = TaskForm()
    return render(request, 'task_edit.html', {'form': form, 'action': action})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    action = 'Update'
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            #msg = 'Task has been edited'
            return redirect('roadmap:task', pk = task.pk)
    else:
        form = TaskEditForm(instance=task)
    return render(request, 'task_edit.html', {'form': form, 'action': action})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    roadmap_pk = task.roadmap.pk
    task.delete()
    return redirect('roadmap:roadmap', pk=roadmap_pk)

def roadmaps_show(request):
    roadmaps = Roadmap.objects.all()
    return render(request, 'roadmaps.html', {'roadmaps': roadmaps})

def roadmap_detail(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk)
    tasks = Task.objects.filter(roadmap=roadmap).order_by('state', 'estimate')
    return render(request, 'roadmap_detail.html', {'roadmap': roadmap, 'tasks': tasks})

def roadmap_new(request):
    if request.method=='POST':
        form = RoadmapForm(request.POST)
        if form.is_valid():
            roadmap = form.save()
            return redirect('roadmap:roadmaps')
    else:
        form = RoadmapForm()
    return render(request, 'roadmap_new.html', {'form': form})

def roadmap_delete(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk)
    roadmap.delete()
    return redirect('roadmap:roadmaps')