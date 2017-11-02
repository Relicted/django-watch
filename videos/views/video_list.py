from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from videos.models import Video


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