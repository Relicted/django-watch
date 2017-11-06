from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from tutorial.storage import OverwriteStorage
from tutorial.models import BaseModel
from videos.uploads import file_picture, videofile_upload


class VideoFile(BaseModel):
    name = models.CharField(
        max_length=150,
        null=True)
    episode = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    video = models.ForeignKey(
        'Video',
        on_delete=models.CASCADE,
        related_name='files')
    season = models.ForeignKey(
        'Season',
        on_delete=models.CASCADE,
        related_name='files',
        blank=True,
        null=True)
    picture = models.ImageField(
        upload_to=file_picture,
        blank=True,)
    file = models.FileField(
        upload_to=videofile_upload,
        storage=OverwriteStorage()
    )

    def __str__(self):
        return self.name

    def get_title(self):
        return self.video.original_title


@receiver(pre_delete, sender=VideoFile)
def videofile_delete(instance, **kwargs):
    """DELETE VIDEO FILES IF VIDEO ITEM WAS DELETED"""
    instance.file.delete(False)
