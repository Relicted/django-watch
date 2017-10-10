import os
from tutorial import settings
import uuid


def videofile_upload(instance, filename):
    """HANDLE VIDEO FILES UPLOAD"""
    fn, fext = os.path.splitext(filename)
    fn = str(instance.video).replace(' ', '').lower()
    return '/'.join([
        settings.VIDEO_FILES,
        '%s-%s%s' % (str(uuid.uuid4()), fn, fext)
    ])


def screen_upload(instance, filename):
    """HANDLE SCREENSHOT UPLOAD"""
    fn, fext = os.path.splitext(filename)
    fn = str(instance.video).replace(' ', '').lower()
    return '/'.join([
        settings.VIDEO_SCREENSHOTS,
        '%s-%s%s' % (fn, str(uuid.uuid4()), fext)
    ])


def poster_upload(instance, filename):
    """HANDLE POSTER UPLOAD"""
    fn, fext = os.path.splitext(filename)
    fn = str(instance).replace(' ', '').lower()
    return '/'.join([
        settings.VIDEO_POSTERS,
        '%s-%s%s' % (fn, str(uuid.uuid4()), fext)])


def wide_poster_upload(instance, filename):
    """HANDLE WIDE_POSTER UPLOAD"""
    fn, fext = os.path.splitext(filename)
    fn = str(instance).replace(' ', '').lower()
    return '/'.join([
        settings.VIDEO_POSTERS_WIDE,
        '%s-%s%s' % (fn, str(uuid.uuid4()), fext)])


def screenshot_handler(file, user=None, fn=None, fext=None):
    """UPLOAD FILES IN TEMP DIR"""
    path = '/'.join([settings.FILE_UPLOAD_TEMP_DIR,
                     user])

    if not os.path.exists(path):
        os.makedirs(path)

    with open('{}/{}{}'.format(path, fn, fext), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

