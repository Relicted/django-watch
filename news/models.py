from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from comments.models import Comment
from tutorial.models import BaseModel, LikeDislike
from .uploads import news_poster_upload

# Create your models here.


class Category(models.Model):
    name = models.CharField(
        max_length=100, primary_key=True)

    def __str__(self):
        return str(self.name)


class Post(BaseModel):
    category = models.ForeignKey(Category)
    article = models.CharField(max_length=300)
    user = models.ForeignKey(User)
    text = models.TextField(max_length=4000)
    votes = GenericRelation(LikeDislike, related_query_name='news')
    main_picture = models.ImageField(upload_to=news_poster_upload)

    comments = GenericRelation(Comment)

    class Meta:
        ordering = ['-created_at']


class PostPicture(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField()
