import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
import sys
# ============================================== #
from tutorial import settings
from .validators import POSTER_SIZE
from tutorial.models import (
    BaseModel,
    LikeDislike)
from .uploads import (
    screen_upload,
    poster_upload,
    wide_poster_upload,
    videofile_upload)
from tutorial.storage import OverwriteStorage


class Video(BaseModel):
    CONTENT_TYPES = (
        ('movies', _('Movies')),
        ('series', _('TV Show')),
        ('animation', _('Animation')),
        ('animationseries', _('Animation Series')),
    )
    SERIES_STATUS = (
        (1, _("On-Going")),
        (2, _("Finished")),
        (3, _("Closed")),
    )

    content = models.CharField(
        choices=CONTENT_TYPES,
        max_length=50,
        null=True)
    series_status = models.PositiveSmallIntegerField(
        choices=SERIES_STATUS,
        blank=True,
        null=True,
        verbose_name='status')
    original_title = models.CharField(
        max_length=150)
    poster = models.ImageField(
        upload_to=poster_upload,
        storage=OverwriteStorage())
    wide_poster = models.ImageField(
        upload_to=wide_poster_upload,
        storage=OverwriteStorage(), )
    description = models.TextField(
        max_length=2000,
        verbose_name='About', )
    votes = GenericRelation(LikeDislike, related_query_name='videos')

    class Meta:
        ordering = ['original_title']
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')

    def __init__(self, *args, **kwargs):
        super(Video, self).__init__(*args, **kwargs)
        self.__original_poster = self.poster
        self.__original_wide_poster = self.wide_poster

        # if self.content != 'series' or self.content != 'animationseries':
        #     self.__serial_status = None

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

        if self.poster != self.__original_poster:
            poster = Image.open(self.poster)
            poster_output = BytesIO()

            poster.thumbnail(POSTER_SIZE)
            poster.save(poster_output, format='JPEG', quality=80)
            poster_output.seek(0)

            if self.id:
                model = Video.objects.get(pk=self.id)
                try:
                    os.remove('/'.join([settings.MEDIA_ROOT,
                                        model.poster.name]))
                except FileNotFoundError:
                    pass

            self.poster = InMemoryUploadedFile(
                poster_output, 'ImageField',
                "%s.jpg" % self.poster.name.split('.')[0],
                'image/jpeg', sys.getsizeof(poster_output), None)

        if self.wide_poster != self.__original_wide_poster:
            wide_poster = Image.open(self.wide_poster)
            wide_output = BytesIO()
            wide_poster.thumbnail(POSTER_SIZE)
            wide_poster.save(wide_output, format='JPEG', quality=80)
            wide_output.seek(0)

            self.wide_poster = InMemoryUploadedFile(
                wide_output, 'ImageField',
                "%s.jpg" % self.wide_poster.name.split('.')[0],
                'image/jpeg', sys.getsizeof(wide_output), None)

        super(Video, self).save(force_insert=False, force_update=False,
                                using=None, update_fields=None)


@receiver(pre_delete, sender=Video)
def posters_delete(instance, **kwargs):
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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        shot = Image.open(self.shot)
        shot_output = BytesIO()
        shot.save(shot_output, format='JPEG', quality=80)
        shot_output.seek(0)

        self.shot = InMemoryUploadedFile(
            shot_output, 'ImageField',
            "%s.jpg" % self.shot.name.split('.')[0],
            'image/jpeg', sys.getsizeof(shot_output), None)

        return super(VideoScreenshot, self).save(force_insert=False,
                                                 force_update=False,
                                                 using=None,
                                                 update_fields=None)


@receiver(pre_delete, sender=VideoScreenshot)
def screenshots_delete(instance, **kwargs):
    """DELETE SHOT FILE IF OBJECT WAS DELETED"""
    instance.shot.delete(False)


class Season(BaseModel):
    number = models.PositiveSmallIntegerField()
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='seasons',
        blank=True,
        null=True)

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
def videofile_delete(instance, **kwargs):
    """DELETE VIDEO FILES IF VIDEO ITEM WAS DELETED"""
    instance.file.delete(False)


class WatchingList(models.Model):
    STATUSES = (
        (1, _("Watching")),
        (2, _("Completed")),
        (3, _("Plan to watch")),
        (4, _("On-hold")),
        (5, _("Dropped")),
        (6, _("Waiting for")),
    )
    SCORES = (
        (1, _('1 - Appalling')),
        (2, _('2 - Horrible')),
        (3, _('3 - Very Bad')),
        (4, _('4 - Bad')),
        (5, _('5 - Average')),
        (6, _('6 - Fine')),
        (7, _('7 - Good')),
        (8, _('8 - Very Good')),
        (9, _('9 - Great')),
        (10, _('10 - Masterpiece')),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True,
        related_name='watchlist')
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='watchlist')
    score = models.PositiveSmallIntegerField(choices=SCORES)
    status = models.PositiveSmallIntegerField(choices=STATUSES)
    is_favorite = models.BooleanField(default=False)
    tags = models.CharField(max_length=500, blank=True, default='')
    comment = models.CharField(max_length=500, blank=True, default='')

    def __str__(self):
        return str(self.score)

    def tag_list(self):
        return self.tags.split(',')