import os
import shutil
from django.core.urlresolvers import resolve
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.utils.translation import ugettext as _
from django.forms.models import model_to_dict
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseRedirect
from django.forms import formset_factory
# create your views here.
from .models import Video, VideoScreenshot, Season, VideoFile
from .forms import (
    CreateVideoItemForm,
    AddScreenshots,
    AddVideoFileForm
)
from tutorial import settings
from .uploads import screenshot_handler

@csrf_exempt
def add_screen(request):
    if not request.is_ajax():
        return HttpResponseRedirect(reverse('video:add'))
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


@method_decorator(login_required, name='dispatch')
class AddVideo(FormView):
    form_class = CreateVideoItemForm
    template_name = 'videos/add_video.html'

    def get_context_data(self, **kwargs):
        context = super(AddVideo, self).get_context_data(**kwargs)
        context['shots'] = AddScreenshots()
        print(Video.objects.all())
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()

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


class VideoList(ListView):
    model = Video
    template_name = 'videos/video_list.html'

    def get(self, request, *args, **kwargs):
        q = [x for x in self.request.path.split('/') if x][-1]
        self.video = Video.objects.filter(content__iexact=q)
        return super(VideoList, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VideoList, self).get_context_data(**kwargs)
        paginator = Paginator(self.video, 10)

        page = self.request.GET.get('page')
        try:
            video = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            video = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            video = paginator.page(paginator.num_pages)
        context['object_list'] = video
        context['paginator'] = paginator
        return context


class VideoDetail(DetailView):
    model = Video
    template_name = 'videos/video_detail.html'

    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        exclude = ['poster', 'wide_poster']
        if request.is_ajax():
            obj = Video.objects.get(pk=request.GET.get('id'))
            response = model_to_dict(obj, exclude=exclude)
            response['like'] = obj.like.count()
            response['dislike'] = obj.like.count()
            data = {
                'response': response
            }
            return JsonResponse(data)
        return super(VideoDetail, self).get(request, *args, **kwargs)


