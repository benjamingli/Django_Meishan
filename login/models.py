from __future__ import unicode_literals

from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=40)
    def __str__(self):
        return "Account: %s" % self.username
