from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class Committee(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)


class Person(models.Model):
    user = models.OneToOneField(User)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    telephone = models.CharField(max_length=10)
    committee = models.ForeignKey(Committee)

    def __unicode__(self):
        return unicode(self.firstName)

    def getKarma(self):
        karma = 0
        for activity in KarmaLog.objects.filter(person=self.pk, active=True):
            task = Task.objects.get(pk=activity.task.pk)
            karma += task.karma
        return karma

    def getTaskList(self, range_start=datetime(2010, 1, 1), range_end=datetime.now):
        tasks = KarmaLog.objects.filter(timeadded__gt=range_start, timeadded__lte=range_end, person=self)
        return tasks


class Task(models.Model):
    description = models.CharField(max_length=100)
    karma = models.IntegerField(default=0)
    recurring = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.description)


class KarmaLog(models.Model):
    person = models.ForeignKey(Person)
    committee = models.ForeignKey(Committee)
    task = models.ForeignKey(Task)
    comment = models.CharField(max_length=2047)
    time = models.DateTimeField(default=datetime.now)
    timeadded = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.pk)

    def getTaskName(self):
        taskName = self.task.description
        return taskName

    def getTaskKarma(self):
        taskKarma = self.task.karma
        return taskKarma

    def getPerson(self):
        return Person.objects.get(firstName=self.person)

    def getCommittee(self):
        return Committee.objects.get(name=self.committee)
