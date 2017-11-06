from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
from tutorial.models import BaseModel
from django.utils.translation import ugettext as _


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=4000)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def get_user_pic(self):
        return self.user.profile.picture.url


class UserMessage(BaseModel):
    TYPES = (
        ('', _('Select Message Type')),
        ('suggestion', _('Suggestion')),
        ('report', _('Report')),
    )

    type = models.CharField(max_length=25, choices=TYPES, null=True)
    theme = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    text = models.CharField(max_length=10000)
    approved = models.BooleanField(default=False)
