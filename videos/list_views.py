from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import WatchingList


class Watchlist(ListView):
    template_name = 'videos/watchlist.html'
    context_object_name = 'pieces'
    model = WatchingList

    def dispatch(self, request, *args, **kwargs):
        if not self.get_queryset():
            return HttpResponseRedirect(reverse('home'))
        return super(Watchlist, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        order = self.request.GET.get('order', 'status')
        self.user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return WatchingList.objects.filter(user=self.user).order_by(order)

    def get_context_data(self, **kwargs):
        print(self.request.GET)
        context = super(Watchlist, self).get_context_data(**kwargs)
        context['model_fields'] = [
            x for x in self.model._meta.get_fields() if x.name != 'id']
        return context
