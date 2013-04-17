from django.core.urlresolvers import resolve
from collections import OrderedDict
from ndc.models import Tag


def menus(request):
    menus = OrderedDict([
        ('timetable', {'title': 'Timetable', 'icon': 'calendar'}),
        ('sessions', {'title': 'Session', 'icon': 'video'}),
        ('speakers', {'title': 'Speaker', 'icon': 'man'}),
        ('companies', {'title': 'Company', 'icon': 'cmd'}),
    ])

    try:
        name = resolve(request.path).url_name
        if name in menus:
            menus[name]['active'] = True
    except:
        pass

    return {
        'menus': menus,
    }


def tags(request):
    return {
        'tags': Tag.objects.all(),
    }


def search(request):
    return {
        'q': request.GET.get('q', ''),
    }
