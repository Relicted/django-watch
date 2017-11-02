from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.forms.models import model_to_dict
from django.views.generic import DetailView
from django.http import JsonResponse
# create your views here.
from comments.models import Comment
from videos.models import Video, WatchingList
from videos.forms import AddVideoToList
from tutorial.models import LikeDislike


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

        content_type = ContentType.objects.get_for_model(Video)
        object_id = self.object.id
        context['comments'] = Comment.objects.filter(
            content_type=content_type,
            object_id=object_id
        ).order_by('-created_at')
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
