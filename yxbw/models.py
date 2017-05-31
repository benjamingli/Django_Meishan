from __future__ import unicode_literals

from django.db import models


class Task(models.Model):
    user = models.CharField(max_length=20)
    time = models.DateTimeField('upload time')
    name = models.CharField(max_length=80)
    fullname = models.CharField(max_length=102)
    accum = models.BooleanField()
    def __str__(self):
        return "Task[%s]" % self.fullname
    class Meta:
        ordering = ['-time']
