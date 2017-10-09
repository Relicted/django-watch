from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.urls import reverse
import sys
# ============================================== #
from.validators import POSTER_SIZE
from tutorial.models import (
    BaseModel,
    BaseModelLike)
from .uploads import (
    screen_upload,
    poster_upload,
    wide_poster_upload,
    videofile_upload)
from tutorial.storage import OverwriteStorage



class Video(BaseModelLike):
    content_types = (
        ('movies', _('Movies')),
        ('series', _('TV Show')),
        ('animation', _('Animation')),
        ('animationseries', _('Animation Series')),
    )

    content = models.CharField(
        choices=content_types,
        max_length=50,
        null=True)
    original_title = models.CharField(
        max_length=150)
    poster = models.ImageField(
        upload_to=poster_upload,
        storage=OverwriteStorage())
    wide_poster = models.ImageField(
        upload_to=wide_poster_upload,
        storage=OverwriteStorage(),)
    description = models.TextField(
        max_length=2000,
        verbose_name='About',)

    class Meta:
        ordering = ['original_title']
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')

    def __str__(self):
        return self.original_title

    def get_absolute_url(self):
        return reverse('video:video_detail',
                       kwargs={
                           'pk': self.pk,
                       })

    def get_admin_url(self):
        return reverse('admin:%s_%s_change' %
                       (self._meta.app_label, self._meta.model_name),
                       args=(self.id,))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        poster = Image.open(self.poster)
        poster_output = BytesIO()

        poster.thumbnail(POSTER_SIZE)
        poster.save(poster_output, format='JPEG', quality=100)
        poster_output.seek(0)

        self.poster = InMemoryUploadedFile(poster_output, 'ImageField',
                                        "%s.jpg" % self.poster.name.split('.')[0],
                                        'image/jpeg', sys.getsizeof(poster_output),
                                        None)

        wide_poster = Image.open(self.wide_poster)
        wide_output = BytesIO()
        wide_poster.thumbnail(POSTER_SIZE)
        wide_poster.save(wide_output, format='JPEG', quality=100)
        wide_output.seek(0)

        self.wide_poster = InMemoryUploadedFile(
            wide_output,'ImageField',
            "%s.jpg" % self.wide_poster.name.split('.')[0],
            'image/jpeg', sys.getsizeof(wide_output), None)

        super(Video, self).save(force_insert=False, force_update=False,
                                using=None, update_fields=None)

    def delete(self, using=None, keep_parents=False):
        self.poster.delete()
        self.wide_poster.delete()
        super(Video, self).delete(using=None, keep_parents=False)


@receiver(pre_delete, sender=Video)
def posters_delete(sender, instance, **kwargs):
    """DELETE POSTERS IF VIDEO OBJECT ITEM WAS DELETED"""
    instance.poster.delete(False)
    instance.wide_poster.delete(False)


class VideoScreenshot(BaseModel):
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='shots')
    shot = models.ImageField(
        upload_to=screen_upload,
        storage=OverwriteStorage())

    class Meta:
        verbose_name = _('Screenshot')
        verbose_name_plural = _("Screenshots")


@receiver(pre_delete, sender=VideoScreenshot)
def screenshots_delete(sender, instance, **kwargs):
    """DELETE SHOT FILE IF OBJECT WAS DELETED"""
    instance.shot.delete(False)


class Season(BaseModel):
    number = models.PositiveSmallIntegerField()
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='seasons')

    def __str__(self):
        return '{}: {} season'.format(self.video.original_title, self.number)


class VideoFile(BaseModel):
    name = models.CharField(
        max_length=150,
        null=True)
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='files')
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='files',
        blank=True,
        null=True)

    file = models.FileField(
        upload_to=videofile_upload,
        storage=OverwriteStorage()
    )

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=VideoFile)
def videofile_delete(sender, instance, **kwargs):
    """DELETE VIDEO FILES IF VIDEO ITEM WAS DELETED"""
    instance.file.delete(False)
