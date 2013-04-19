# -*- coding:utf-8 -*-
from django.template.loader import get_template
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
        text, 'NDC13 팬페이지 <ez@smartstudy.co.kr>',
        [token.email])
    msg.attach_alternative(html, "text/html")

    try:
        msg.send(fail_silently=True)
    except:
        pass
