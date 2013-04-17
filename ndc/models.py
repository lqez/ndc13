from django.db import models
from django.utils.safestring import mark_safe
from datetime import datetime


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

    class Meta:
        ordering = ['name']

    def get_sessions(self):
        return Session.objects.filter(speakers__in=self.speaker_set.all())

    def __unicode__(self):
        return self.name


class Speaker(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    email = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    company = models.ForeignKey(Company, null=True)

    class Meta:
        ordering = ['name']

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
