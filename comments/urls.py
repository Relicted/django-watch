from django.conf.urls import url
from .views import user_messages

urlpatterns = [
    url(r'^$', user_messages, name='messages'),
]