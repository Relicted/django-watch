
import os
import uuid
from tutorial import settings

def news_poster_upload(instance, filename):
    fn, fext = os.path.splitext(filename)
    fn = str(instance.article).replace(' ', '-').lower()
    return '/'.join([
        settings.NEWS_POSTER,
        '%s-%s%s' % (str(uuid.uuid4()), fn, fext)
    ])