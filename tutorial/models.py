from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .managers import LikeDislikeManager

class BaseModel(models.Model):
    """ABSTRACT MODEL ADD DATES OF CREATION AND UPDATE"""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_(u'Creation date'))
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_(u'Edited date')
    )

    objects = models.Manager()

    class Meta:
        abstract = True


class LikeDislike(BaseModel):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (LIKE, _('Like')),
        (DISLIKE, _('Dislike'))
    )

    vote = models.IntegerField(
        verbose_name='vote',
        choices=VOTES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

    class Meta:
        app_label = 'accounts'

