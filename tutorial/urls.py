from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from accounts.views import profile_view
from news.models import Post
from tutorial.models import LikeDislike
from videos.models import Video
from .views import Home, SearchResult, Votes

urlpatterns = [
    # ADMIN
    url(r'^admin/', admin.site.urls),

    # HOMEPAGE SEARCH
    url(r'^$', Home.as_view(), name='home'),
    url(r'^search/$', SearchResult.as_view(), name='search-result'),

    # LIKES
    url(r'^video/(?P<pk>\d+)/like/$',
        login_required(Votes.as_view(model=Video, vote_type=LikeDislike.LIKE)),
        name='video_like'),
    url(r'^video/(?P<pk>\d+)/dislike/$',
        login_required(Votes.as_view(model=Video, vote_type=LikeDislike.DISLIKE)),
        name='video_dislike'),
    url(r'post/(?P<pk>\d+)/like/$',
        login_required(Votes.as_view(model=Post, vote_type=LikeDislike.LIKE)),
        name='post_like'),
    url(r'^post/(?P<pk>\d+)/dislike/$',
        login_required(Votes.as_view(model=Post, vote_type=LikeDislike.DISLIKE)),
        name='post_dislike'),


    # VIDEO
    url(r'^video/', include('videos.urls', namespace='video')),
    url(r'^list/', include('videos.list_urls', namespace='list')),

    # NEWS
    url(r'^news/', include('news.urls', namespace='news')),

    # REGISTRATION, LOGIN, Profiles
    url(r'^accounts/', include('accounts.auth.urls', namespace='account')),
    url(r'^settings/', include('accounts.urls', namespace='settings')),

]


if settings.DEBUG:
    try:
        urlpatterns += [
            url(r'^devtest/', include('devtest.urls', namespace='test')),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    except:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += [
    url(r'^(?P<profile>[a-zA-Z0-9]+)/$', profile_view, name='profile')
]