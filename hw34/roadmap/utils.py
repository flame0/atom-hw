from datetime import date, timedelta, datetime
from django.db import models
from roadmap.models import Score
from calendar import monthrange


def monday_of_week_one(yyyy):
    """ Method to calculate date for Monday of first week of year

    >>> monday_of_week_one(1970)
    datetime.date(1969, 12, 29)
    """

    ref_day = date(yyyy, 1, 4)
    dow = ref_day.weekday()
    monday = ref_day - timedelta(days=dow)

    return monday


def stats(roadmaps):
    weeks = []
    #cur_month = datetime.now().month
    cur_year = datetime.now().year
    init_date = monday_of_week_one(cur_year)
    for i in range(0, 52):
        from_date = init_date
        to_date = init_date + timedelta(days=6)
        title = from_date.strftime("%Y-%m-%d") + ' / ' + to_date.strftime("%Y-%m-%d")
        weeks.append({'from_date': from_date,
                      'to_date': to_date,
                      'tasks_completed': 0,
                      'tasks_created': 0,
                      'title': title,
                      'number': i + 1})
        init_date = init_date + timedelta(days=7)
    for roadmap in roadmaps:
        for week in weeks:
            tasks_created = roadmap.task_set.filter(created__range=(week['from_date'], week['to_date']))
            tasks_completed = roadmap.task_set.filter(score__date__range=(week['from_date'], week['to_date']))
            week['tasks_created'] += tasks_created.count()
            week['tasks_completed'] += tasks_completed.count()

    months = []
    #init_date = monday_of_week_one(datetime.now().year)
    for i in range(1, 13):
        from_date = datetime(cur_year, i, 1)
        to_date = datetime(cur_year, i, monthrange(cur_year, i)[1])
        months.append({'from_date': from_date,
                       'to_date': to_date,
                       'title': from_date.strftime("%Y-%m"),
                       'points_earned': 0})

    for roadmap in roadmaps:
        for month in months:
            scores = Score.objects.filter(task__roadmap=roadmap, date__range=(month['from_date'], month['to_date']))
            points_earned = scores.aggregate(models.Sum('points'))['points__sum']
            if points_earned is None:
                points_earned = 0
            month['points_earned'] += points_earned

    return {"weeks": weeks, "months": months}


def dev(a, b):
    if b == 0:
        return
    return a / b

