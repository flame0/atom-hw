from datetime import datetime
from django.utils import timezone
from django.db import models
from django.db.models import Max, F, DurationField
from datetime import date, time, timedelta
from account.models import Account


class Roadmap(models.Model):
    name = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

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
    state = models.CharField(max_length=12, choices=STATE_CHOICES, default='in_progress')
    estimate = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)

    def set_score(self):
        #max_estimate = Task.objects.all().annotate(maximum=models.Max(models.ExpressionWrapper(
         #   models.F('estimate') - models.F('created'),
          #  output_field=models.DurationField())))[0]
        max_estimate = Task.objects.all().aggregate(maximum=Max(F('estimate') - F('created'),
                                                                  output_field=DurationField()))
        today = timezone.now()
        points = (today - self.created) / (self.estimate - self.created) + (
                                                (self.estimate - self.created) / max_estimate['maximum'])
        if not hasattr(self, 'score'):
            self.score = Score.objects.create(task=self, points=points)
        else:
            self.score.points = points

    def unset_score(self):
        print(self.score)
        if self.score is not None:
            self.score.delete()

    @property
    def remaining(self):
        """Remains until expiration of the deadline"""
        if self.state == "in_progress":
            return self.estimate - timezone.now()
        else:
            return timedelta(0)

    @property
    def is_failed(self):
        """return true if task is failed"""
        if self.state == "in_progress" and self.estimate < timezone.now():
            return True
        else:
            return False

    @property
    def is_crit(self):
        if self.remaining <= timedelta(days=3) and self.state == 'in_progress' or self.is_failed:
            return True
        else:
            return False

    def __str__(self):
        return self.title


class Score(models.Model):
    task = models.OneToOneField(Task, primary_key=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    points = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return 'Score for ' + self.task.title
