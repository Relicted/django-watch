from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from videos.models import Video
from django.contrib.contenttypes.models import ContentType
from .models import LikeDislike


class Home(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['serials'] = Video.objects.filter(
            content='series').order_by('-updated_at')[:6]
        context['movies'] = Video.objects.filter(
            content='movies').order_by('-updated_at')[:6]
        return context


class SearchResult(ListView):
    template_name = 'home/search_result.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        return Video.objects.filter(
            Q(original_title__icontains=q) |
            Q(description__icontains=q)
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super(SearchResult, self).get_context_data(**kwargs)

        return context


class Votes(View):
    model = None
    vote_type = None

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        try:
            likedislike = LikeDislike.objects.get(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
                user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
            else:
                likedislike.delete()
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)

        data = {
            'likes': obj.votes.likes().count(),
            'dislikes': obj.votes.dislikes().count(),
            'sum_rating': obj.votes.sum_rating()
        }

        return JsonResponse(data, content_type='application/json')