from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse
# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView
from videos import models
from comments.models import Comment
from news.forms import CreatePostForm
from videos.models import Video
from .models import Post, Category
from django.db.models import Q


class ListNews(ListView):
    template_name = 'news/news_list.html'
    context_object_name = 'list'
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        print('got post request', request.POST)
        data={}
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super(ListNews, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name')
        return context

    def get_queryset(self):
        q = self.request.GET.get('cat')
        search = self.request.GET.get('search')
        if q:
            cat = Category.objects.get(pk=q)
            return Post.objects.filter(category=cat)
        if search:
            return Post.objects.filter(
                Q(article__icontains=search) |
                Q(text__icontains=search)
            )

        return Post.objects.all().order_by('-created_at')


class PostDetail(DetailView):
    template_name = 'news/post_detail.html'
    context_object_name = 'post'
    model = Post

    # PEREDELAI SOZDANIE KOMMENTOV
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('account:login'))
        Comment.objects.create(
            user=request.user,
            text=request.POST.get('comment'),
            content_type=ContentType.objects.get_for_model(Post),
            object_id=kwargs.get('pk')
        )
        return HttpResponseRedirect(
            reverse('news:post_detail', kwargs=kwargs)
        )

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        content_type = ContentType.objects.get_for_model(Post)
        object_id = self.object.id
        context['comments'] = Comment.objects.filter(
            content_type=content_type,
            object_id=object_id
        ).order_by('-created_at')
        return context


@method_decorator(login_required, name='dispatch')
class CreatePost(CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'news/create_post.html'

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()

        if self.request.POST.getlist('video'):
            for x in self.request.POST.getlist('video'):

                obj = Video.objects.get(pk=int(x))
                instance.videos.add(obj)
        # instance.videos.add(x for x in self.request.POST.getlist('videos'))
        form.save_m2m()

        return HttpResponseRedirect(self.get_success_url())