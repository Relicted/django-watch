from django.conf.urls import url
from .views import Watchlist

urlpatterns = [
    url('^(?P<username>[a-zA-Z0-9]+)/$', Watchlist.as_view(), name='watchlist'),
]