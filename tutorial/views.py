from django.views.generic import TemplateView, ListView
from django.db.models import Q
from videos.models import Video


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