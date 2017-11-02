from django.contrib import admin

from news.models import Post, Category

admin.site.register(Category)
admin.site.register(Post)
