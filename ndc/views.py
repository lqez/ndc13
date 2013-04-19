from django.contrib.auth import login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from models import SessionDate, SessionTime, Room, Session, Speaker, Company, Tag, EmailToken, Comment
from forms import EmailLoginForm, ProfileForm
from helper import sendEmailToken, render_json, render_template_json


def home(request):
    return render(request, 'home.html')


def login(request):
    form = EmailLoginForm()

    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            # Remove previous tokens
            email = form.cleaned_data['email']
            EmailToken.objects.filter(email=email).delete()

            # Create new
            token = EmailToken(email=email)
            token.save()

            sendEmailToken(request, token)
            return redirect(reverse_lazy('login_mailsent'))

    return render(request, 'login.html', {
        'form': form,
    })


def login_req(request, token):
    token = get_object_or_404(EmailToken, token=token)
    email = token.email

    try:
        user = User.objects.get(email=email)
    except:
        user = User.objects.create_user(email, email, token)
        user.save()

        profile = user.get_profile()
        profile.nick = email.split('@')[0]
        profile.save()

    token.delete()

    # Set backend manually
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    user_login(request, user)

    return redirect(reverse_lazy('profile'))


def login_mailsent(request):
    return render(request, 'login_mailsent.html')


def logout(request):
    user_logout(request)
    return redirect(reverse_lazy('home'))


@login_required
def profile(request):
    form = ProfileForm(instance=request.user.get_profile())

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = request.user.get_profile()
            profile.nick = form.cleaned_data['nick']
            profile.use_gravatar = form.cleaned_data['use_gravatar']
            profile.save()

    return render(request, 'profile.html', {
        'form': form,
    })


@login_required
def comment(request):
    if request.is_ajax():
        try:
            msg = request.POST.get('msg', '')[:255]
            if len(msg) == 0:
                raise

            cid = request.POST.get('cid')
            ctype = request.POST.get('ctype')

            if ctype == 'session':
                Comment(user=request.user, msg=msg, session=Session.objects.get(id=cid)).save()
            elif ctype == 'speaker':
                Comment(user=request.user, msg=msg, speaker=Speaker.objects.get(id=cid)).save()

            return render_json({
                'success': True,
            })
        except:
            pass

    return render_json({
        'success': False,
    })


def comments(request, ctype, cid, page):
    comments = []
    print ctype, cid

    if ctype == 'session':
        comments = Comment.objects.filter(session=cid, removed=False).select_related()[:20]
    elif ctype == 'speaker':
        comments = Comment.objects.filter(speaker=cid, removed=False).select_related()[:20]

    return render_template_json('json/comments.json', {
        'user': request.user,
        'comments': comments,
    })


def timetable(request):
    cache_key = 'timetable_context'
    context_cache = cache.get(cache_key)

    if not context_cache:
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

        context_cache = {
            'wide': wide,
            'narrow': narrow,
            'rooms': rooms,
            'tags': Tag.objects.all(),
        }

        cache.set(cache_key, context_cache, 60 * 60)

    return render(request, 'timetable.html', context_cache)


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
