from django.core.urlresolvers import resolve
from collections import OrderedDict


def menus(request):
    menus = OrderedDict([
        ('home', {'title': 'Timetable'}),
        ('sessions', {'title': 'Session'}),
        ('speakers', {'title': 'Speaker'}),
        ('companies', {'title': 'Company'}),
        ('links', {'title': 'Link'}),
        ('about', {'title': 'About'}),
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
