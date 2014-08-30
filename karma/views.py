from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from karma.models import Person, KarmaLog, Committee, Task

#In de index staat een tabel met alle personen, en hoeveel karmapunten ze hebben
@login_required()
def index(request):
    persons = Person.objects.all()
    committees = Committee.objects.all()
    context = {
        'persons': persons,
        'committees': committees
    }
    return render(request, 'karma/index.html', context)

@login_required()
def personView(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    tasks = reversed(KarmaLog.objects.filter(person=person.pk))
    taskOverview = Task.objects.all()
    committees = Committee.objects.all()
    context = {
        'person': person,
        'taskOverview': taskOverview,
        'tasks': tasks,
        'committees': committees
    }
    return render(request, 'karma/personView.html', context)

@login_required()
def committeeView(request, committeeName):
    committees = Committee.objects.all()
    committeeSelected = Committee.objects.get(name=committeeName)
    tasks = reversed(KarmaLog.objects.filter(committee=committeeSelected.pk))
    context = {
        'committeeSelected': committeeSelected,
        'committees': committees,
        'tasks': tasks
    }
    return render(request, 'karma/committeeView.html', context)

@login_required()
def addTask(request, person_name):
    comment = request.POST["comment"] if request.POST["comment"] != "comment" else ""
    taskselect = request.POST["taskselect"]
    committee_id = request.POST["committeeSelect"]
    if taskselect == "nieuw_task":
        omschrijving = request.POST["Omschrijving"]
        karma = request.POST["karma"]
        tk=Task.objects.filter(description=omschrijving)
        if tk < 1:
            task = Task(description=omschrijving, karma=karma)
            task.save()
        else:
            return HttpResponseRedirect('karma:yousuck')
    else:
        task = Task.objects.get(pk=taskselect)
    committee = get_object_or_404(Committee, pk=committee_id)
    person = get_object_or_404(Person, firstName=person_name)

    taskToAdd = KarmaLog(person=person, committee=committee, task=task, comment=comment)
    taskToAdd.save()
    return HttpResponseRedirect(reverse('karma:personView', args=(person.pk,)))

def yousuck(request):
    return HttpResponse("You did something horribly wrong. Try again. Perhaps the activity you are trying to add already exists?")