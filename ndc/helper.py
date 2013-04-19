# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.utils import simplejson as json
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives


def sendEmailToken(request, token):
    variables = Context({
        'request': request,
        'token': token,
    })
    html = get_template('mail/token_html.html').render(variables)
    text = get_template('mail/token_text.html').render(variables)

    msg = EmailMultiAlternatives(
        'NDC13 팬페이지 로그인 링크입니다.',
        text, 'NDC13 팬페이지 관리자 <ez@smartstudy.co.kr>',
        [token.email])
    msg.attach_alternative(html, "text/html")

    try:
        msg.send(fail_silently=True)
    except:
        pass


def render_json(data_dict):
    return HttpResponse(json.dumps(data_dict), 'application/javascript')


def render_template_json(template, context):
    return HttpResponse(render_to_string(template, context), 'application/javascript')
