from datetime import date, datetime, timedelta


class Task:
    states = frozenset(["in_progress", "ready"])

    def __init__(self, title, estimate, state="in_progress"):
        self.title = title
        self.estimate = estimate
        self.state = state

    def __repr__(self):
        return "<{}:{} - {}>".format(self.title, self.state, self.estimate)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        assert type(val) is str, "title is not a string: %r" % val
        self._title = val

    @property
    def estimate(self):
        return self._estimate

    @estimate.setter
    def estimate(self, val):
        assert type(val) is date, "estimate is not a date: %r" % val
        self._estimate = val

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        assert val in self.states, "state is not in states list"
        self._state = val

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

    def ready(self):
        """change state to ready"""
        self.state = "ready"


class Roadmap:

    def __init__(self, tasks=[]):
        self.tasks = tasks

    def filter(self, state):
        return [task for task in self.tasks if task.state == state]

    def crit(self):
        """ Print Crit tasks """
        return [task for task in self.tasks if task.remaining <= timedelta(days=3) and task.state == "in_progress" or task.is_failed]

    @property
    def today(self):
        """ return list of tasks where task estimate == today"""
        return [task for task in self.tasks if task.estimate == date.today()]



def __main():
    """Test for Task and Roadmap classes"""
    tasks = []
    states = ['ready', 'in_progress']
    for i in range(30):
        tasks.append(Task("Task#{}".format(i), date(2017, 4, i+1), states[i % 2]))
    for i in range(30):
        tasks.append(Task("Task#{}".format(30+i), date(2017, 3, i+1), states[i % 2]))
    road = Roadmap(tasks)

    print("================Today tasks=============\n")
    for task in road.today:
        print("Title:{} Estimate:{} State:{}".format(task.title, task.estimate, task.state))
    print("================Crit tasks=============\n")
    for task in road.crit():
        print("Title:{} Estimate:{} State:{}".format(task.title, task.estimate, task.state))
    print("================In Progress tasks=============\n")
    for task in road.filter('in_progress'):
        print("Title:{} Estimate:{} State:{}".format(task.title, task.estimate, task.state))
    print("================All faild tasks=============\n")
    for task in road.tasks:
        if task.is_failed:
            print("Title:{} Estimate:{} State:{}".format(task.title, task.estimate, task.state))


if __name__ == "__main__":
    __main()
