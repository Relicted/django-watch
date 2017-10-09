from django.conf.urls import url, include
from .views import (CustomLoginView,
                    logout_view,
                    activation_view,
                    CustomRegistrationView)

urlpatterns = [
    #MAIN PAGE
    url(r'^login/$', CustomLoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),

    url(r'^register/$',
        CustomRegistrationView.as_view(),
        name="registration"),

    url(r'^activation/', activation_view, name='activation'),

    url(r'^', include('registration.backends.hmac.urls')),
    #SEARCH


]