from django.forms import ModelForm, SelectDateWidget,ValidationError
from roadmap.models import Task, Roadmap
from datetime import date, time


class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['title', 'state', 'estimate', 'roadmap']
		widgets = {
			'estimate': SelectDateWidget(years=range(2000,2050)),
		}

	def clean_estimate(self):
		estimate = self.cleaned_data['estimate']
		if  estimate < date.today():
			raise ValidationError("Estimate must be today or later")

class RoadmapForm(ModelForm):
	class Meta:
		model = Roadmap
		fields = ['name']