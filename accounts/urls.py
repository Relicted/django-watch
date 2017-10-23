from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from .views import (profile_view,
                    profile,
                    account)

urlpatterns = [
    #profile settings
    url(r'^$', RedirectView.as_view(
        url=reverse_lazy('settings:profile'), permanent=True)),

    url(r'^profile/$', profile, name='profile'),
    url(r'^account/$', account, name='account'),

]