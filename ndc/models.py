from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='tag', blank=True, null=True)


class Room(models.Model):
    name = models.CharField(max_length=100)


class SessionDate(models.Model):
    day = models.DateField()


class SessionTime(models.Model):
    begin = models.TimeField()
    end = models.TimeField()


class Company(models.Model):
    name = models.CharField(max_length=100, db_index=True)


class Speaker(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    email = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    company = models.ForeignKey(Company, null=True)


class Session(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    desc = models.CharField(max_length=2000, null=True, blank=True, db_index=True)
    slide_url = models.CharField(max_length=255, null=True, blank=True)
    speakers = models.ManyToManyField(Speaker)

    room = models.ForeignKey(Room)
    date = models.ForeignKey(SessionDate)
    times = models.ManyToManyField(SessionTime)
