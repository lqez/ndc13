from django.db.models import F
from django.http import HttpResponseNotAllowed
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.utils import simplejson
from ndc.models import *


def home(request):
    dates = SessionDate.objects.all()
    times = SessionTime.objects.all()
    rooms = Room.objects.all()

    table = {}
    for d in dates:
        table[d] = {}
        for t in times:
            table[d][t] = {}
            for r in rooms:
                s = Session.objects.filter(date=d, times=t, room=r)
                if s:
                    if s[0].times.all()[0] == t:
                        table[d][t][r] = s[0]
                else:
                    table[d][t][r] = None

    return render(request, 'home.html', {
        'dates': dates,
        'times': times,
        'rooms': rooms,
        'table' : table,
    })


class speaker_list(ListView):
    model = Speaker


class speaker_detail(DetailView):
    model = Speaker


class session_list(ListView):
    model = Session


class session_detail(DetailView):
    model = Session
