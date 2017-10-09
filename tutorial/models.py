from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

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


class BaseModelLike(BaseModel):
    """ABSTRACT MODEL WITH LIKE/DISLIKE FIELDS"""
    like = models.ManyToManyField(
        User,
        blank=True,
        editable=False,
        related_name='likes'
    )
    dislike = models.ManyToManyField(
        User,
        blank=True,
        editable=False,
        related_name='dislikes'
    )

    class Meta:
        abstract = True
