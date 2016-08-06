# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


USER_STATUS_CHOICES = (
    (0, "active"),
)

@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    login = models.CharField(max_length=60, default="")
    url = models.URLField(max_length=100, blank=True)
    activation_key = models.CharField(max_length=60, default="0")
    status = models.IntegerField(default=0, choices=USER_STATUS_CHOICES)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class UserMeta(models.Model):
    """
    Meta information about a user.
    """

    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, related_name="meta", blank=True, null=True)
    key = models.CharField(max_length=255)
    value = models.TextField()

    def __unicode__(self):
        return u"%s: %s" % (self.key, self.value)
