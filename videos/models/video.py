from django.contrib.contenttypes.fields import GenericRelation
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils.translation import ugettext as _
from PIL import Image
from tutorial.models import BaseModel, LikeDislike
from django.db import models
from videos.uploads import poster_upload
from tutorial.storage import OverwriteStorage
import os
import sys
from tutorial import settings
from io import BytesIO
from videos.validators import POSTER_SIZE


class Genre(BaseModel):
    genre = models.CharField(max_length=150,
                             primary_key=True)

    class Meta:
        ordering = ['genre']

    def __str__(self):
        return self.genre


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
    genres = models.ManyToManyField('Genre')
    poster = models.ImageField(
        upload_to=poster_upload,
        storage=OverwriteStorage())
    description = models.TextField(
        max_length=2000,
        verbose_name='About', )
    votes = GenericRelation(LikeDislike, related_query_name='videos')
    news = models.ManyToManyField('news.Post', related_name='videos')

    class Meta:
        ordering = ['original_title']
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')

    def __init__(self, *args, **kwargs):
        super(Video, self).__init__(*args, **kwargs)
        self.__original_poster = self.poster

    def __str__(self):
        return self.original_title

    def get_absolute_url(self):
        return reverse('video:video_detail',
                       kwargs={
                           'pk': self.pk,
                       })

    def get_last_news(self):
        return self.news.order_by('-created_at')[:6]

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

        super(Video, self).save(force_insert=False, force_update=False,
                                using=None, update_fields=None)


@receiver(pre_delete, sender=Video)
def posters_delete(instance, **kwargs):
    """DELETE POSTERS IF VIDEO OBJECT ITEM WAS DELETED"""
    instance.poster.delete(False)


class Season(BaseModel):
    number = models.PositiveSmallIntegerField()
    video = models.ForeignKey(
        'Video',
        on_delete=models.CASCADE,
        related_name='seasons',
        blank=True,
        null=True)

    def __str__(self):
        return '{}: {} season'.format(self.video.original_title, self.number)

