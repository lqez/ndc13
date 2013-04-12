from django.db.models import F
from django.http import HttpResponseNotAllowed
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.utils import simplejson
from ndc.models import *


def home(request):
    return render(request, 'home.html')


class speaker_list(ListView):
    model = Speaker


class speaker_detail(DetailView):
    model = Speaker


class session_list(ListView):
    model = Session


class session_detail(DetailView):
    model = Session

