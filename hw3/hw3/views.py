from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import TaskForm
import datetime

def task_form(request):
	if request.method =='POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			post = form.save()
			msg = 'Post have been created. '
			return render(request, 'form.html', {'msg': msg} )
	else:
		form = TaskForm()
	return render(request, 'form.html', {'form': form})