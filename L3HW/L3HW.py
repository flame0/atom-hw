from datetime import date, datetime, timedelta

class Task:
    states = frozenset(["in_progress", "ready"])
    state=property()
    def __init__(self, title, estimate, state="in_progress"):
    	assert type(title) is str, "title is not a string: %r" % name
    	assert type(estimate) is date, "estimate is not a date: %r" % estimate
    	assert type(state) is str, "state is not a str: %r" % state
        self.estimate = estimate
        self.state = state            

    def __repr__(self):
        return "<{}:{} - {}>".format(self.title, self.state, self.estimate)

    def _state(self,val):
    	assert val in self.states, "state is not in states list"
    	self.state = val

    def _remaining(self):
        """Remains until expiration of the deadline"""
        if self.state == "in_progress":
            return self.estimate - date.today()
        else:
            return timedelta(0)

    def _is_failed(self):
        """return true if task is failed"""
        if self.state == "in_progress" and self.estimate < date.today():
            return True
        else:
            return False

    def ready(self):
        """change state to ready"""
        self.state = "ready"

    remaining = property(_remaining)
    is_failed = property(_is_failed)

class Roadmap:
    def __init__(self, tasks=[]):
        self.tasks = tasks

    def filter(self, state):
        return [task for task in tasks if task.state == state]

    def _today(self):
        """ return list of tasks where task estimate == today"""
        return [task for task in tasks if task.estimate == date.today()]
    today = property(_today)
