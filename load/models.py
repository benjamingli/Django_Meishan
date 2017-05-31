from __future__ import unicode_literals

from django.db import models


class Weather(models.Model):
    date = models.DateField('date')
    holiday = models.IntegerField('holiday', default=0)
    maxTemp = models.IntegerField('maxTemp', default=0)
    minTemp = models.IntegerField('minTemp', default=0)
    typeDay = models.IntegerField('typeDay', default=0)
    def __str__(self):
        return "Weather[%s]" % self.date
    class Meta:
        ordering = ['-date']

class RawCsv(models.Model):
    user = models.CharField(max_length=20)
    time = models.DateTimeField('upload time')
    filename = models.CharField(max_length=80)
    fullname = models.CharField(max_length=102)
    def __str__(self):
        return "RawCsv[%s]" % self.fullname
    class Meta:
        ordering = ['filename']

class Data(models.Model):
    user = models.CharField(max_length=20)
    time = models.DateTimeField('generate time')
    filename = models.CharField(max_length=80)
    fullname = models.CharField(max_length=102)
    def __str__(self):
        return "Data[%s]" % self.fullname
    class Meta:
        ordering = ['filename']

class Result(models.Model):
    user = models.CharField(max_length=20)
    time = models.DateTimeField('generate time')
    data = models.CharField(max_length=80)
    date = models.DateField('date')
    prefix = models.CharField(max_length=122)
    n = models.IntegerField('.name line count')
    def __str__(self):
        return "Result[%s]" % self.prefix
    class Meta:
        ordering = ['-time']

