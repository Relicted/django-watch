import os
import shutil
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.core.files import File
from django.utils.translation import ugettext as _
from django.forms.models import model_to_dict
from django.views.generic import DetailView, ListView, FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseRedirect
# create your views here.
from .models import Video, VideoScreenshot, Season, VideoFile, WatchingList
from .forms import (
    CreateVideoItemForm,
    AddScreenshots,
    AddVideoFileForm,
    AddVideoToList
)
from tutorial.models import LikeDislike
from tutorial import settings
from .uploads import screenshot_handler


def watching_now(request, pk):
    post = [x for x in request.POST if x != 'csrfmiddlewaretoken']
    defaults = {k: request.POST.get(k) for k in post}

    try:
        if defaults['is_favorite']:
            defaults['is_favorite'] = True
    except KeyError:
        defaults['is_favorite'] = False

    if request.method == 'POST':
        list_item, created = WatchingList.objects.update_or_create(
            defaults=defaults,
            user=request.user,
            video=Video.objects.get(pk=pk)
        )
        return HttpResponseRedirect(reverse('video:video_detail', kwargs={'pk':pk}))
    else:
        return HttpResponseRedirect(reverse('home'))


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
    video = None

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
    watchlists = None

    def get_context_data(self, **kwargs):
        context = super(VideoDetail, self).get_context_data(**kwargs)
        self.watchlists = WatchingList.objects.filter(
            video=self.object
        )
        if self.watchlists:
            votes = self.watchlists.count()
            context['score'] = round(sum(
                [x.score for x in self.watchlists]) / votes, 1)
            context['votes'] = votes

        try:
            context['in_list'] = self.watchlists.get(
                user=self.request.user,
                video=self.object
            )
        except (WatchingList.DoesNotExist,
                AttributeError,
                TypeError):
            pass

        if self.request.user.is_authenticated():
            context['list_add_form'] = AddVideoToList(
                instance=WatchingList.objects.filter(
                    user=self.request.user,
                    video=self.object).first())
        context['test'] = LikeDislike.objects.all().count()
        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            fields = ['original_title', 'description']
            obj = Video.objects.get(pk=request.GET.get('id'))

            response = model_to_dict(obj, fields=fields)

            data = {
                'like': obj.votes.likes().count(),
                'like_url': reverse('video_like', kwargs={'pk': obj.pk}),
                'dislike': obj.votes.dislikes().count(),
                'dislike_url': reverse('video_dislike', kwargs={'pk': obj.pk}),
            }

            return JsonResponse({**response, **data})
        return super(VideoDetail, self).get(request, *args, **kwargs)


