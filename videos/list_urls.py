from django.conf.urls import url
from .views import (
    VideoList, VideoDetail, AddVideo, add_screen, watching_now)
from .list_views import (Watchlist,)

urlpatterns = [
    url('^(?P<pk>\d+)/$', Watchlist.as_view(), name='watchlist'),
]