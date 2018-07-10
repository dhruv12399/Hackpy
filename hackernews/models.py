# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Link(models.Model):
	title = models.CharField(max_length = 200)
	url = models.URLField(max_length = 400)
	parent = models.CharField(max_length = 100)
	votes = models.IntegerField(default = 1)
	added_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'added_by')
	added_time = models.DateTimeField(default = timezone.now)
	score = models.FloatField(default = 0.0)
	upvoted_users = models.ManyToManyField(settings.AUTH_USER_MODEL, null = True, blank = True, related_name = 'upvoted_users')

	def __str__(self):
		return self.title


class Comments(models.Model):
	content = models.TextField()
	linked_to = models.ForeignKey(Link)
	parent = models.ForeignKey('self', null = True,blank = True)
	added_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	added_time = models.DateTimeField(default = timezone.now)
