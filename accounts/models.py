import sys
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from videos.models import Video
from tutorial.storage import OverwriteStorage
from django.db.models.signals import post_save
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

    def __str__(self):
        return self.user.username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_picture = self.picture

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.__original_picture != self.picture and self.picture:
            pic = Image.open(self.picture)
            print(pic)
            pic_output = BytesIO()

            pic.thumbnail((300, 300))
            pic.save(pic_output, format='JPEG')
            pic_output.seek(0)

            self.picture = InMemoryUploadedFile(
                pic_output, 'ImageField',
                "%s%s" % (os.path.splitext(self.picture.name)),
                'image/jpeg', sys.getsizeof(pic_output), None)

            if self.id:
                model = Profile.objects.get(pk=self.id)
                try:
                    if model.picture.name.split('.')[0] == 'default_':
                        raise FileNotFoundError(
                            'File with "default_" name is an exception'
                        )
                    os.remove('/'.join([settings.MEDIA_ROOT,
                                        model.picture.name]))
                except FileNotFoundError:
                    pass

        elif not self.picture:
            self.picture = content_file_name(self, None)

        super(Profile, self).save(force_insert=False,
                                  force_update=False,
                                  using=None,
                                  update_fields=None)


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)