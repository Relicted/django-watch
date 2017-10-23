from django.conf.urls import url
from .views import (CustomRegistrationView,
                    CustomLoginView,
                    logout_view,
                    activation_view)


urlpatterns = [
    #
    url(r'^login/$',
        CustomLoginView.as_view(),
        name='login'),
    url(r'^logout/$', logout_view, name='logout'),

    url(r'^register/$',
        CustomRegistrationView.as_view(),
        name="registration"),

    url(r'^activation/$', activation_view, name='activation'),
]