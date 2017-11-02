from django.views.generic import ListView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from videos.models import WatchingList


class Watchlist(ListView):
    template_name = 'videos/watchlist.html'
    context_object_name = 'pieces'
    model = WatchingList

    def get_queryset(self):
        order = self.request.GET.get('order', 'status')
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return WatchingList.objects.filter(user=user).order_by(order)

    def get_context_data(self, **kwargs):
        context = super(Watchlist, self).get_context_data(**kwargs)
        context['model_fields'] = [
            x for x in self.model._meta.get_fields() if x.name != 'id']
        return context
