from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
from reportlab.pdfgen import canvas
from django.template import Context
from django.template.loader import get_template
from subprocess import Popen, PIPE
from TempDir import TemporaryDirectory
from datetime import datetime, date
import os
import tempfile

from karma.models import Person, KarmaLog, Committee, Task

@login_required()
def karmaHome(request):
    user = request.user
    person = Person.objects.get(user=request.user)
    return HttpResponseRedirect(reverse('karma:personView', args=(person.pk,)))

#In de index staat een tabel met alle personen, en hoeveel karmapunten ze hebben
@login_required()
def index(request):
    persons = Person.objects.all()
    persons = sorted(persons, key=lambda person: person.firstName)
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
    tasks = reversed(KarmaLog.objects.filter(person=person.pk, active=True).order_by('time'))
    taskOverview = Task.objects.filter(recurring=True)
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
    tasks = reversed(KarmaLog.objects.filter(committee=committeeSelected.pk, active=True).order_by('time'))
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
    taskTime = request.POST["datetime"]
    if taskselect == "nieuw_task":
        omschrijving = request.POST["Omschrijving"]
        karma = request.POST["karma"]
        if "recurring" in request.POST:
            recurring = True
        else:
            recurring = False
        tk = Task.objects.filter(description=omschrijving, recurring=True)
        if len(tk) == 0:
            task = Task(description=omschrijving, karma=karma, recurring=recurring)
            task.save()
        else:
            return HttpResponse("You did something horribly wrong. Perhaps the activity you are trying to add already exists?")
    else:
        task = Task.objects.get(pk=taskselect)
    committee = get_object_or_404(Committee, pk=committee_id)
    person = get_object_or_404(Person, pk=person_id)
    taskToAdd = KarmaLog(person=person, committee=committee, task=task, comment=comment, time=taskTime)
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

def overviewstart(request):
    context = {
        'now': datetime.now()
    }
    return render(request, 'karma/overviewstart.html', context)

def overviewgenpdf(request):
    #range_start = request.POST["range_start"]
    #range_end = request.POST["range_end"]
    range_start = datetime(2012, 01, 01)
    range_end = datetime(2014, 12, 24)
    persons = Person.objects.all()
    for person in persons:
        person.tasks = KarmaLog.objects.filter(timeadded__gt=range_start, timeadded__lte=range_end, person=person)
        for task in person.tasks:
            task.time = task.time.date()
    context = Context({
            'start_date': range_start.date(),
            'end_date': range_end.date(),
            'persons': persons,
        })
    template = get_template('overview_template.tex')
    rendered_tpl = template.render(context).encode('utf-8')

    # Python3 only. For python2 check out the docs!
    with TemporaryDirectory() as tempdir:
        # Create subprocess, supress output with PIPE and
        # run latex twice to generate the TOC properly.
        # Finally read the generated pdf.
        for i in range(2):
            process = Popen(
                ['pdflatex', '-output-directory', tempdir],
                stdin=PIPE,
                stdout=PIPE,
            )
            process.communicate(rendered_tpl)
        with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
            pdf = f.read()

    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename=' + 'texput.pdf'
    response.write(pdf)
    return response


def yousuck(request, person_id):
    return HttpResponse("You did something horribly wrong. Perhaps the activity you are trying to add already exists?")
