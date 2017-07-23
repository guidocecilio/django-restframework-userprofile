# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Topic(models.Model):
  name = models.CharField(max_length=12)
  description = models.CharField(max_length=100, blank=True)


class Profile(models.Model):
    # full_name = models.CharField(max_length=128)
    # email = models.CharField(max_length=100)
    current_position = models.CharField(max_length=64)
    about_you = models.CharField(max_length=255, blank=True, default='')
    favorite_topics = models.ManyToManyField(
        Topic,
        # through='FavoriteTopics',
        # through_fields=('topic', 'userprofile'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # class Meta:
    #     ordering = ('created',)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class FavoriteTopics(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

