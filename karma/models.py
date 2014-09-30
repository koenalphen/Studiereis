from django.db import models
from django.contrib.auth.models import User
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
    email = models.CharField(max_length=100)
    telephone = models.CharField(max_length=10)
    committee = models.ForeignKey(Committee)

    def __unicode__(self):
        return unicode(self.firstName)

    def getKarma(self):
        karma = 0
        for activity in KarmaLog.objects.filter(person=self.pk, active=True):
            task = Task.objects.get(description=activity.task)
            karma += task.karma
        return karma


class Task(models.Model):
    description = models.CharField(max_length=100)
    karma = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.description)


class KarmaLog(models.Model):
    person = models.ForeignKey(Person)
    committee = models.ForeignKey(Committee)
    task = models.ForeignKey(Task)
    comment = models.CharField(max_length=2047)
    time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.pk)

    def getTaskName(self):
        task = Task.objects.get(description=self.task)
        return task.description

    def getTaskKarma(self):
        task = Task.objects.get(description=self.task)
        return task.karma

    def getPerson(self):
        return Person.objects.get(firstName=self.person)

    def getCommittee(self):
        return Committee.objects.get(name=self.committee)