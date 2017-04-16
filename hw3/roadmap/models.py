from django.db import models
from datetime import date, time, timedelta


class Roadmap(models.Model):
	name = models.CharField(max_length=100)

	def today(self):
		today_tasks = Task.objects.filter(estimate=date.today(), roadmap=self)
		return today_tasks

	def filter(self, state):
		state_tasks = Task.objects.filter(state=state, roadmap=self)
		return state_tasks

	def __str__(self):
		return self.name

class Task(models.Model):
	STATE_CHOICES = [
		('in_progress', 'In progress'),
		('ready', 'Ready')
	]

	title = models.CharField(max_length=100)
	state = models.CharField(max_length=12, choices = STATE_CHOICES)
	estimate = models.DateField()
	roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)

	@property
	def remaining(self):
		"""Remains until expiration of the deadline"""
		if self.state == "in_progress":
			return self.estimate - date.today()
		else:
			return timedelta(0)

	@property
	def is_failed(self):
		"""return true if task is failed"""
		if self.state == "in_progress" and self.estimate < date.today():
			return True
		else:
			return False

	def __str__(self):
		return self.title