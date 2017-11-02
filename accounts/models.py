import datetime
import secrets
import sys
import uuid
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from tutorial.models import BaseModel
from videos.models import Video
from tutorial.storage import OverwriteStorage
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import os
from io import BytesIO
from PIL import Image
from tutorial import settings


def content_file_name(instance, filename):
    if filename:
        fn, fext = os.path.splitext(filename)
        fn = instance.user.id
        filename = '%s%s' % (str(fn), str(fext))
        return '/'.join(['profile_pictures', filename])
    else:
        return '/'.join(['profile_pictures', 'default_.png'])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(
        upload_to=content_file_name,
        storage=OverwriteStorage(),
        blank=True)
    name = models.CharField(max_length=150, blank=True)
    bio = models.CharField(max_length=2000, blank=True)
    skype = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=50, blank=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_picture = self.picture

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # CHECK IF PICTURE FIELD CHANGED
        if self.__original_picture != self.picture and self.picture:
            pic = Image.open(self.picture)
            pic_output = BytesIO()

            pic.thumbnail((300, 300))
            ext = self.picture.name.split('.')[-1]
            if ext.lower() == 'jpg':
                ext = 'JPEG'
            pic.save(pic_output, format=ext)
            pic_output.seek(0)

            self.picture = InMemoryUploadedFile(
                pic_output, 'ImageField',
                "%s%s" % (os.path.splitext(self.picture.name)),
                'image/jpeg', sys.getsizeof(pic_output), None)

            # DELETE OLD PICTURE ON CHANGE
            if self.id:
                model = Profile.objects.get(pk=self.id)
                try:
                    pic_name = model.picture.name
                    if pic_name == content_file_name(self, None):
                        raise FileNotFoundError
                    os.remove('/'.join([settings.MEDIA_ROOT,
                                        model.picture.name]))
                except FileNotFoundError:
                    pass
        # SET DEFAULT PICTURE IF NO PIC SELECTED
        elif not self.picture:
            self.picture = content_file_name(self, None)

        super(Profile, self).save(force_insert=False,
                                  force_update=False,
                                  using=None,
                                  update_fields=None)


@receiver(post_save, sender=User)
def update_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class PasswordResetLink(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(primary_key=True,
                            max_length=176,
                            unique=True)

    def __str__(self):
        return str(self.created_at)

    def code_valid(self):
        time = (timezone.now() - self.created_at).days

        if time < settings.PASSWORD_RESET_TIMEOUT_DAYS:
            return True
        self.delete()
        return False


@receiver(pre_save, sender=PasswordResetLink)
def remove_expired(**kwarg):
    codes = PasswordResetLink.objects.all()
    for code in codes:
        code.code_valid()

