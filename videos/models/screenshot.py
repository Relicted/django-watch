from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
from django.db import models
from django.utils.translation import ugettext as _
import sys
# ============================================== #
from tutorial.models import BaseModel
from videos.uploads import screen_upload
from tutorial.storage import OverwriteStorage


class VideoScreenshot(BaseModel):
    video = models.ForeignKey(
        'Video',
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

        if self.shot.name.split('.')[-1] == 'jpg':
            ext = 'jpeg'
        else:
            ext = self.shot.name.split('.')[-1]

        shot.save(shot_output, format=f'{ext}', quality=80)
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