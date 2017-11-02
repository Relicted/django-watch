import os
import shutil
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.http import JsonResponse
# create your views here.
from tutorial import settings


def screenshot_handler(file, user=None, fn=None, fext=None):
    """UPLOAD FILES IN TEMP DIR"""
    path = '/'.join([settings.FILE_UPLOAD_TEMP_DIR,
                     user])

    if not os.path.exists(path):
        os.makedirs(path)

    with open(f'{path}/{fn}{fext}', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def add_screen(request):
    """
    LOOP THROUGH ALL FILES IN POST REQUEST
    UPLOAD EACH FILE TO TEMP
    """
    if not request.is_ajax():
        return redirect('video:add')

    user = request.user.username
    path = '/'.join([settings.FILE_UPLOAD_TEMP_DIR,
                     user])
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)

    data = {}

    if request.method == "POST":
        files = request.FILES.getlist('files')
        if len(files) > 10:
            return JsonResponse(data={'errors': _('Max_length 10')})
        else:
            for num, value in enumerate(files):
                fn, fext = os.path.splitext(value.name)
                fn = num
                screenshot_handler(value, user=user, fn=fn, fext=fext)
        return JsonResponse(data)

