from django.conf.urls import url
from .views import VideoView, VideoDetail, AddVideo, add_screen

urlpatterns = [

    # video lists
    url(r'^movies/$', VideoView.as_view(), name='movie'),
    url(r'^series/$', VideoView.as_view(), name='series'),
    url(r'^animation/$', VideoView.as_view(), name='animation'),
    url(r'^animationseries/$', VideoView.as_view(), name='animationseries'),
    #add new video item
    url(r'^add/$', AddVideo.as_view(), name='add'),
    url(r'^add/screenshot/$', add_screen, name='screen_upload'),
    #video item detail
    url(r'^item/(?P<pk>[0-9]+)/$',
        VideoDetail.as_view(),
        name='video_detail'),
]
