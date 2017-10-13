from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required

from tutorial.models import LikeDislike
from videos.models import Video
from .views import Home, SearchResult, Votes

app_name = 'ajax'

urlpatterns = [
    # ADMIN
    url(r'^admin/', admin.site.urls),
    #HOMEPAGE SEARCH
    url(r'^$', Home.as_view(), name='home'),
    url(r'^search/', SearchResult.as_view(), name='search-result'),

    #LIKES
    url(r'^video/(?P<pk>\d+)/like/$',
        login_required(Votes.as_view(model=Video, vote_type=LikeDislike.LIKE)),
        name='video_like'),
    url(r'^video/(?P<pk>\d+)/dislike/$',
        login_required(Votes.as_view(model=Video, vote_type=LikeDislike.DISLIKE)),
        name='video_dislike'),

    # REGISTRATION, LOGIN, ETC
    url(r'^accounts/', include('accounts.urls', namespace='account')),
    #VIDEO
    url(r'^video/', include('videos.urls', namespace='video')),
    url(r'^videolist/', include('videos.list_urls', namespace='list')),

]


if settings.DEBUG:
    try:
        urlpatterns += [
            url(r'^devtest/', include('devtest.urls', namespace='test')),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    except:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)