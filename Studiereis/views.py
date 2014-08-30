from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from karma.models import Person, KarmaLog, Committee, Task

# TODO update style base.html

def index(request):
    # TODO write a generic view, linking to karma and polls
    committees = Committee.objects.all()
    context = {
        'committees': committees
    }
    return render(request, 'base.html', context)