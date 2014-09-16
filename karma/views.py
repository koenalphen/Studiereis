from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from karma.models import Person, KarmaLog, Committee, Task

@login_required()
def karmaHome(request):
    user = request.user
    return HttpResponseRedirect(reverse('karma:personView', args=(user.pk,)))

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

@csrf_protect
@login_required()
def personView(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    tasks = reversed(KarmaLog.objects.filter(person=person.pk, active=True))
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
    tasks = reversed(KarmaLog.objects.filter(committee=committeeSelected.pk, active=True))
    context = {
        'committeeSelected': committeeSelected,
        'committees': committees,
        'tasks': tasks
    }
    return render(request, 'karma/committeeView.html', context)

@login_required()
def addTask(request, person_id):
    comment = request.POST["comment"] if request.POST["comment"] != "comment" else ""
    taskselect = request.POST["taskselect"]
    committee_id = request.POST["committeeSelect"]
    if taskselect == "nieuw_task":
        omschrijving = request.POST["Omschrijving"]
        karma = request.POST["karma"]
        tk = Task.objects.filter(description=omschrijving)
        if len(tk) == 0:
            task = Task(description=omschrijving, karma=karma)
            task.save()
        else:
            return HttpResponse("You did something horribly wrong. Perhaps the activity you are trying to add already exists?")
    else:
        task = Task.objects.get(pk=taskselect)
    committee = get_object_or_404(Committee, pk=committee_id)
    person = get_object_or_404(Person, pk=person_id)

    taskToAdd = KarmaLog(person=person, committee=committee, task=task, comment=comment)
    taskToAdd.save()
    return HttpResponseRedirect(reverse('karma:personView', args=(person.pk,)))

@csrf_protect
@login_required()
def removeTask(request):
    taskToRemove_id = request.POST["taskToRemove_id"]
    #taskToRemove = KarmaLog.objects.filter(pk=taskToRemove_id)
    taskToRemove = get_object_or_404(KarmaLog, pk=taskToRemove_id)
    print(taskToRemove)
    taskToRemove.active = False
    taskToRemove.save()
    print("succes!")



def yousuck(request, person_id):
    return HttpResponse("You did something horribly wrong. Perhaps the activity you are trying to add already exists?")