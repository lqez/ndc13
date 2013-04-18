from django.db import models
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime
import string
import random


class Tag(models.Model):
    name = models.CharField(max_length=100)
    uid = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='tag', blank=True, null=True)
    is_category = models.BooleanField(default=False)

    def html(self):
        return mark_safe('<div id=\'%s\' class=\'tag tag-%s tag-icon-%s\'>%s</div>' % (self.uid, self.uid, self.uid, self.name))

    def __unicode__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class SessionDate(models.Model):
    day = models.DateField()

    def sessions(self):
        return Session.objects.filter(date=self)

    def __unicode__(self):
        return self.day.strftime("%m/%d (%a)")


class SessionTime(models.Model):
    begin = models.TimeField()
    end = models.TimeField()

    def _todatetime(self, time):
        return datetime.today().replace(hour=time.hour, minute=time.minute, second=time.second,
                                        microsecond=time.microsecond, tzinfo=time.tzinfo)

    def duration_in_min(self):
        return (self._todatetime(self.end) - self._todatetime(self.begin)).seconds / 60

    def __unicode__(self):
        return '%s - %s' % (self.begin, self.end)


class Company(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    desc = models.CharField(max_length=2000, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('company', args=[self.id])

    def get_tags(self):
        return Tag.objects.filter(id__in=self.get_sessions().values_list('tags', flat=True))

    def get_classes(self):
        return set([_ for sublist in [_.get_classes() for _ in self.get_sessions()] for _ in sublist])

    def get_sessions(self):
        return Session.objects.filter(speakers__in=self.speaker_set.all())

    def __unicode__(self):
        return self.name


class Speaker(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    email = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    company = models.ForeignKey(Company, null=True)

    class Meta:
        ordering = ['name']

    def get_twitter_link(self):
        return mark_safe('<a href="https://twitter.com/%s" target="_blank">@%s</a>' % (self.twitter, self.twitter))

    def get_twitter_profile_image(self):
        return mark_safe('http://api.twitter.com/1/users/profile_image/?screen_name=%s&size=bigger' % self.twitter)

    def get_absolute_url(self):
        return reverse('speaker', args=[self.id])

    def get_tags(self):
        return Tag.objects.filter(id__in=Session.objects.filter(speakers=self).values_list('tags', flat=True))

    def get_classes(self):
        return set([_ for sublist in [_.get_classes() for _ in Session.objects.filter(speakers=self)] for _ in sublist])

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.company)


class Session(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    desc = models.CharField(max_length=2000, null=True, blank=True, db_index=True)
    slide_url = models.CharField(max_length=255, null=True, blank=True)
    speakers = models.ManyToManyField(Speaker, blank=True)
    tags = models.ManyToManyField(Tag)

    room = models.ForeignKey(Room)
    date = models.ForeignKey(SessionDate)
    times = models.ManyToManyField(SessionTime)

    def get_absolute_url(self):
        return reverse('session', args=[self.id])

    def duration_in_min(self):
        r_min = sum([_.duration_in_min() for _ in self.times.all()])
        return 25 if r_min < 50 else 50

    def is_keynote(self):
        if self.tags.filter(uid="keynote"):
            return True
        return False

    def begin_time(self):
        return self.times.all()[0].begin.strftime("%H:%M")

    def get_times(self):
        times = self.times.all()
        return '%s - %s' % (times[0].begin.strftime("%H:%M"),
                            times[len(times) - 1].end.strftime("%H:%M"))

    def get_companies(self):
        # set() does not preserve the original order. So I made a poop :(
        uniq = []
        for s in self.speakers.all():
            if s.company not in uniq:
                uniq.append(s.company)
        return uniq

    def get_category_tags(self):
        return self.tags.filter(is_category=True)

    def get_classes(self):
        return ['ft-' + _.uid for _ in self.get_category_tags()]

    def html_get_category_tags(self):
        return mark_safe(''.join([_.html() for _ in self.get_category_tags()]))

    def html_get_speakers(self):
        return ', '.join([_.name for _ in self.speakers.all()])

    def html_get_companies(self):
        return ', '.join([_.name for _ in self.get_companies()])

    def __unicode__(self):
        return self.name


class EmailToken(models.Model):
    email = models.EmailField(max_length=255)
    token = models.CharField(max_length=64, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    def id_generator(self, size=64, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    def save(self, *args, **kwargs):
        self.token = self.id_generator()
        super(EmailToken, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    nick = models.CharField(max_length=255, null=True, blank=True)
    use_gravatar = models.BooleanField(default=True)

    def html_profile_image(self):
        if self.use_gravatar:
            import hashlib
            hashed = hashlib.md5(self.user.email.lower()).hexdigest()
            return mark_safe('<div class="gravatar"><img src="http://www.gravatar.com/avatar/%s/?s=48"/></div>' % hashed)
        else:
            return mark_safe('<span class="fui-man-24"></span>')


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
