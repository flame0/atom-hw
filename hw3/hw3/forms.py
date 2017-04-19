from django.forms import ModelForm
from roadmap.models import Task, Roadmap

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['title', 'state', 'estimate', 'roadmap']

class RoadmapForm(ModelForm):
	class Meta:
		model = Roadmap
		fields = ['name']