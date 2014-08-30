from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from karma.models import Person, KarmaLog, Committee, Task

def index(request):
    committees = Committee.objects.all()
    context = {
        'committees': committees
    }
    return render(request, 'base.html', context)