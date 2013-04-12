from django.db.models import F
from django.http import HttpResponseNotAllowed
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, DetailView
from django.utils import simplejson


def home(request):
    return render(request, 'home.html')
