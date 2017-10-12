from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from .views import Home, SearchResult


urlpatterns = [
    # ADMIN
    url(r'^admin/', admin.site.urls),
    #HOMEPAGE SEARCH
    url(r'^$', Home.as_view(), name='home'),
    url(r'^search/', SearchResult.as_view(), name='search-result'),
    # REGISTRATION, LOGIN, ETC

    url(r'^accounts/', include('accounts.urls', namespace='account')),
    #VIDEO
    url(r'^video/', include('videos.urls', namespace='video')),

]

if settings.DEBUG:
    try:
        urlpatterns += [
            url(r'^devtest/', include('devtest.urls', namespace='test')),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    except:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)