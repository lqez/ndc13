from django.db.models import F
from django.http import HttpResponseNotAllowed
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.utils import simplejson
from ndc.models import *


def home(request):
    return render(request, 'home.html', {})


def timetable(request):
    dates = SessionDate.objects.all()
    times = SessionTime.objects.all()
    rooms = Room.objects.all()

    wide = {}
    narrow = {}
    for d in dates:
        wide[d] = {}
        narrow[d] = {}
        for t in times:
            wide[d][t] = {}
            narrow[d][t] = {}
            for r in rooms:
                s = Session.objects.filter(date=d, times=t, room=r)
                if s:
                    if s[0].times.all()[0] == t:
                        wide[d][t][r] = s[0]
                        narrow[d][t][r] = s[0]
                else:
                    wide[d][t][r] = None

            if len(narrow[d][t]) == 0:
                del(narrow[d][t])


    return render(request, 'timetable.html', {
        'wide': wide,
        'narrow': narrow,
        'rooms': rooms,
        'tags': Tag.objects.all(),
    })


def search(request):
    return render(request, 'search.html', {})


def about(request):
    return render(request, 'about.html', {})


class company_list(ListView):
    model = Company


class company_detail(DetailView):
    model = Company


class speaker_list(ListView):
    model = Speaker


class speaker_detail(DetailView):
    model = Speaker


class session_list(ListView):
    model = Session

    def get_context_data(self, **kwargs):
        context = super(session_list, self).get_context_data(**kwargs)
        context['dates'] = SessionDate.objects.all()
        return context


class session_detail(DetailView):
    model = Session
