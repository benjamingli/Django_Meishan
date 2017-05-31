from __future__ import unicode_literals

from django.db import models


class Task(models.Model):
    user = models.CharField(max_length=20)
    time = models.DateTimeField('upload time')
    name = models.CharField(max_length=80)
    fullname = models.CharField(max_length=102)
    hourT = models.IntegerField('hour threshold', default=10)
    dayT = models.IntegerField('day threshold', default=30)
    overT = models.FloatField('over threshold', default=1.6)
    def __str__(self):
        return "Task[%s-%s]" % (self.user, self.name)
    class Meta:
        ordering = ['-time']
