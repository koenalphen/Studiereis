from django.shortcuts import render, get_object_or_404

from karma.models import Person, KarmaLog, Committee

#In de index staat een tabel met alle personen, en hoeveel karmapunten ze hebben
def index(request):
    persons = Person.objects.all()
    committees = Committee.objects.all()
    context = {
        'persons': persons,
        'committees': committees
    }
    return render(request, 'karma/index.html', context)

def personView(request, person_name):
    person = get_object_or_404(Person, firstName = person_name)
    tasks = KarmaLog.objects.filter(person=person.pk)
    committees = Committee.objects.all()
    context = {
        'person': person,
        'tasks': tasks,
        'committees': committees
    }
    return render(request, 'karma/personView.html', context)

def committeeView(request, committeeName):
    committees = Committee.objects.all()
    committeeSelected = Committee.objects.get(name=committeeName)
    tasks = KarmaLog.objects.filter(committee=committeeSelected.pk)
    context = {
        'committeeSelected': committeeSelected,
        'committees': committees,
        'tasks': tasks
    }
    return render(request, 'karma/committeeView.html', context)

def addTask(request, person_id):
    pass