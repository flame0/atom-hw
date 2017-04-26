from django.test import TestCase
from .models import Task,Roadmap,Score
# Create your tests here.
class ScoreTestCase(TestCase):
    def setUp(self):
        road = Roadmap("Test1")
        task1= Task()