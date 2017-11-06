from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from tutorial.models import BaseModel, LikeDislike
from .uploads import news_poster_upload
from django.utils.translation import ugettext as _
# Create your models here.


class Category(BaseModel):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    def get_url_name(self):
        return self.name.replace(' ', '').lower()


class Post(BaseModel):
    category = models.ManyToManyField(Category)
    article = models.CharField(max_length=100)
    description = models.CharField(max_length=600, null=True)
    user = models.ForeignKey(User)
    text = models.TextField(max_length=10000)
    votes = GenericRelation(LikeDislike, related_query_name='news')
    main_picture = models.ImageField(upload_to=news_poster_upload,
                                     verbose_name=_('Upload Picture'))

    comments = GenericRelation(Comment)

    class Meta:
        ordering = ['-created_at']


class PostPicture(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField()
