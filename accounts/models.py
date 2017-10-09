from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from videos.models import Video
from tutorial.storage import OverwriteStorage
from django.db.models.signals import post_save
from django.dispatch import receiver
import os


def content_file_name(instance, filename):
    if filename:
        fn, fext = os.path.splitext(filename)
        fn = instance.user.id
        filename = '%s.png' % str(fn)
        return '/'.join(['profile_pictures', filename])
    else:
        return '/'.join(['profile_pictures', 'default_.png'])




