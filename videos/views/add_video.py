import os
import shutil
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.core.files import File
from django.views.generic import FormView
from django.http import HttpResponseRedirect
# create your views here.
from videos.models import VideoScreenshot, Season
from videos.forms import CreateVideoItemForm

from tutorial import settings


@method_decorator(login_required, name='dispatch')
class AddVideo(FormView):
    form_class = CreateVideoItemForm
    template_name = 'videos/add_video.html'

    def get_context_data(self, **kwargs):
        context = super(AddVideo, self).get_context_data(**kwargs)
        context['screen_ajax_url'] = reverse('video:screen_upload')
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        shots_dir = '/'.join([
            settings.FILE_UPLOAD_TEMP_DIR,
            self.request.user.username
        ])
        try:
            for picture in os.listdir(shots_dir):
                file_path = '/'.join([shots_dir, picture])
                pic = open(file_path, 'rb')
                VideoScreenshot.objects.create(
                    video=instance,
                    shot=File(pic)
                )
            shutil.rmtree(shots_dir, ignore_errors=True)
        except FileNotFoundError:
            pass

        for season in self.request.POST.getlist('season'):
            Season.objects.create(
                video=instance,
                number=season
            )
        return HttpResponseRedirect(self.get_success_url(video=instance))

    def get_success_url(self, video):
        return reverse('video:video_detail', kwargs={'pk': video.id})