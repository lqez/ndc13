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

    return render(request, 'timetable.html', {
        'table': table,
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

    def get_context_data(self, **kwargs):
        context = super(speaker_list, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class speaker_detail(DetailView):
    model = Speaker


class session_list(ListView):
    model = Session

    def get_context_data(self, **kwargs):
        context = super(session_list, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['dates'] = SessionDate.objects.all()
        return context


class session_detail(DetailView):
    model = Session
