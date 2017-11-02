from django.conf.urls import url
from .views import (CustomRegistrationView,
                    CustomLoginView,
                    logout_view,
                    activate,
                    password_reset,
                    complete_reset)


urlpatterns = [
    #
    url(r'^login/$',
        CustomLoginView.as_view(),
        name='login'),
    url(r'^logout/$', logout_view, name='logout'),

    url(r'^register/$',
        CustomRegistrationView.as_view(),
        name="registration"),

    url(r'^password_reset/$', password_reset, name='password_reset'),
    # PASSWORD RESET LINK
    url(r'^password_reset/(?P<token>[0-9a-zA-Z]+)/$',
        complete_reset, name='complete_reset'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

]