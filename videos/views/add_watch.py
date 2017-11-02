from django.shortcuts import redirect, reverse
from videos.models import Video, WatchingList

def add_watch(request, pk):
    post = [x for x in request.POST if x != 'csrfmiddlewaretoken']
    defaults = {k: request.POST.get(k) for k in post}
    success_url = reverse('video:video_detail', kwargs={'pk': pk})

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
        return redirect(success_url)
    else:
        return redirect('home')