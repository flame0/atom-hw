from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TaskForm
from roadmap.models import Task, Roadmap
import datetime

def task_detail(request, pk):
	task = get_object_or_404(Task, pk=pk)
	return render(request, 'task.html', {'task': task})

def task_new(request):
	action = 'New'
	if request.method =='POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			task = form.save() #post?
			#msg = 'Task has been created. '
			empty_form = TaskForm()
			return redirect('task', pk = task.pk)
			#return render(request, 'task_edit.html', {'form': empty_form, 'action': action ,'msg': msg} )
	else:
		form = TaskForm()
	return render(request, 'task_edit.html', {'form': form, 'action': action})

def task_update(request, pk):
	task = get_object_or_404(Task, pk=pk)
	action = 'Update'
	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			task = form.save()
			#msg = 'Task has been edited'
			return redirect('task', pk = task.pk)
	else:
		form = TaskForm(instance=task)
	return render(request, 'task_edit.html', {'form': form, 'action': action})
