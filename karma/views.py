from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
from reportlab.pdfgen import canvas
from django.template import Context
from django.template.loader import get_template
from subprocess import Popen, PIPE
from TempDir import TemporaryDirectory
from datetime import datetime, date, timedelta, time
from isoweek import Week
from django.utils import simplejson
from django.conf import settings
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

@csrf_protect
@login_required()
def overviewstart(request):
    committees = Committee.objects.all()
    context = {
        'committees': committees,
        'now': datetime.now(),
    }
    return render(request, 'karma/overviewstart.html', context)

@csrf_protect
@login_required()
def overviewgenpdf(request):
    range_start = request.POST["range_start"]
    range_end = request.POST["range_end"]
    #range_start = datetime(2012, 01, 01)
    #range_end = datetime(2014, 12, 24)
    range_start = datetime.strptime(range_start, '%Y-%m-%d')
    range_end = datetime.strptime(range_end, '%Y-%m-%d')

    persons = Person.objects.all()
    for person in persons:
        person.totalKarma = 0
        person.tasks = KarmaLog.objects.filter(timeadded__gt=range_start, timeadded__lte=range_end, person=person)
        for task in person.tasks:
            task.time = task.time.date()
            person.totalKarma += task.task.karma
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

@csrf_protect
@login_required()
@user_passes_test(lambda u: u.is_staff)
def charts(request):
    committees = Committee.objects.all()
    tasks = KarmaLog.objects.filter(active=True).order_by('time')
    numTasks = len(tasks)
    year = tasks[0].time.isocalendar()[0]  # get year of first task
    startDate = tasks[0].time.isocalendar()[1]  # get weeknumber of first task
    endDate = tasks[numTasks - 1].time.isocalendar()[1] + 52 * (tasks[numTasks - 1].time.isocalendar()[0] - tasks[0].time.isocalendar()[0])  # get time of last task
    weekmodifier = 0
    timelabels = []
    karmaPerWeek = []
    for week in range(startDate, endDate+1):
        karmaThisWeek = 0
        monday = datetime.combine(Week(year, week - weekmodifier).monday(), time.min)
        sunday = datetime.combine(Week(year, week - weekmodifier).sunday(), time.max)
        logsThisWeek = tasks.filter(time__gt=monday, time__lte=sunday)
        for log in logsThisWeek:
            karmaThisWeek += log.task.karma
        karmaPerWeek.append(karmaThisWeek)
        timelabels.append(week - weekmodifier)
        if week == 52:
            weekmodifier += 52
            year += 1

    lineChartData = {
        'labels': timelabels,
        'datasets':
            [
                {
                    'label': "Karma per week",
                    'fillColor': "rgba(220,220,220,0.2)",
                    'strokeColor': "rgba(220,220,220,1)",
                    'pointColor': "rgba(220,220,220,1)",
                    'pointStrokeColor': "#fff",
                    'pointHighlightFill': "#fff",
                    'pointHighlightStroke': "rgba(220,220,220,1)",
                    'data': karmaPerWeek,
                }
            ]
        }

    # Code to generate the "per activity" chart
    categoryLabels = []
    karmaPerCategory = []
    # recurring tasks
    categories = Task.objects.filter(recurring=True)
    for category in categories:
        categoryLabels.append(category.description)
        logs = tasks.filter(task=category)
        karmaPerCategory.append(category.karma * len(logs))
    # other tasks
    otherTasks = Task.objects.filter(recurring=False)
    otherKarma = 0
    for task in otherTasks:
        otherKarma += task.karma
    categoryLabels.append('Overig')
    karmaPerCategory.append(otherKarma)

    perTaskData = {
        'labels': categoryLabels,
        'datasets':
            [
                {
                    'label': "My First dataset",
                    'fillColor': "rgba(220,220,220,0.5)",
                    'strokeColor': "rgba(220,220,220,0.8)",
                    'highlightFill': "rgba(220,220,220,0.75)",
                    'highlightStroke': "rgba(220,220,220,1)",
                    'data': karmaPerCategory
                }
            ]
        }


    # Code to generate the "per committee" chart
    committeeLabels = []
    karmaPerCommittee = []
    for committee in committees:
        committeeKarma = 0
        committeeLabels.append(committee.name)
        logs = tasks.filter(committee=committee)
        for task in logs:
            committeeKarma += task.task.karma
        karmaPerCommittee.append(committeeKarma)

    perCommitteeData = {
        'labels': committeeLabels,
        'datasets':
            [
                {
                    'label': "My First dataset",
                    'fillColor': "rgba(220,220,220,0.5)",
                    'strokeColor': "rgba(220,220,220,0.8)",
                    'highlightFill': "rgba(220,220,220,0.75)",
                    'highlightStroke': "rgba(220,220,220,1)",
                    'data': karmaPerCommittee
                }
            ]
        }



    lineData = simplejson.dumps(lineChartData)
    perTaskDataJson = simplejson.dumps(perTaskData)
    perCommitteeDataJson = simplejson.dumps(perCommitteeData)

    context = {
        'committees': committees,
        'lineData': lineData,
        'perTaskData': perTaskDataJson,
        'perCommitteeData': perCommitteeDataJson,
    }
    return render(request, 'karma/Charts.html', context)

