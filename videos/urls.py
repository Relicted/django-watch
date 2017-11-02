from django.conf.urls import url

from .views import (
    VideoList, VideoDetail, AddVideo, add_screen, add_watch)

urlpatterns = [

    # video lists
    url(r'^movies/$', VideoList.as_view(), name='movie'),
    url(r'^series/$', VideoList.as_view(), name='series'),
    url(r'^animation/$', VideoList.as_view(), name='animation'),
    url(r'^animationseries/$', VideoList.as_view(), name='animationseries'),
    #add new video item
    url(r'^add/$', AddVideo.as_view(), name='add'),
    url(r'^add/screenshot/$', add_screen, name='screen_upload'),
    #video item detail
    url(r'^item/(?P<pk>[0-9]+)/$',
        VideoDetail.as_view(),
        name='video_detail'),


    #favorites
    url(r'^watching/(?P<pk>[0-9]+)', add_watch, name='watching'),
]
