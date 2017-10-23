from django.conf.urls import url
from django.views.generic import CreateView

from .views import ListNews, CreatePost, PostDetail


urlpatterns = [
    url(r'^$', ListNews.as_view(), name='list_news'),
    url(r'^(?P<pk>[0-9]+)/$', PostDetail.as_view(), name='post_detail'),
    url(r'^create/$', CreatePost.as_view(), name='post_create')
]