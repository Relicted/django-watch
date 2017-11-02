import os
from tutorial import settings
import uuid


def videofile_upload(instance, filename):
    """HANDLE VIDEO FILES UPLOAD"""
    fn, fext = os.path.splitext(filename)
    content = instance.video.content
    video = str(instance.video.pk)
    fn = f'{instance.name}{fext}'

    try:
        season = f'S{str(instance.season.number)}'
        return '/'.join([settings.VIDEO_FILES,
                         content,
                         video,
                         season,
                         fn])
    except AttributeError:
        return '/'.join([settings.VIDEO_FILES,
                         content,
                         video,
                         fn])


def file_picture(instance, filename):
    fn, fext = os.path.splitext(filename)
    video = instance.video.original_title
    name = instance.name
    try:
        season = instance.season.number
        fn = f'{video}-{season}-{name}{fext}'
    except AttributeError:
        fn = f'{video}-{name}{fext}'


    return '/'.join([settings.VIDEO_FILE_PICTURE, fn])



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
