# Create your views here.
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import View
from taggit.models import Tag

from hitcount.views import HitCountDetailView

from ojoalplato.blog.models import Post
from ojoalplato.category.models import Category
from ojoalplato.users.models import User


class PostList(ListView):
    model = Post
    template_name = 'blog/wpfamily/post_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.published()

    def get(self, request, **kwargs):
        if request.GET.get("p"):
            post_id = request.GET.get("p")
            slug = get_object_or_404(Post, id=post_id).slug
            return redirect(reverse("post-detail", kwargs={"slug": slug}))
        else:
            return super(ListView, self).get(request, **kwargs)


class PostDetail(HitCountDetailView):
    model = Post
    template_name = 'blog/wpfamily/post_detail.html'
    count_hit = True


class PostDetailById(View):
    def get(self, request, pk):
        slug = get_object_or_404(Post, id=pk).slug
        return redirect(reverse("post-detail", kwargs={"slug": slug}))


class CategoryList(ListView):
    model = Post
    template_name = 'blog/wpfamily/category_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['category'])

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context["category"] = get_object_or_404(Category, slug=self.kwargs['category']).name
        return context


class TagList(ListView):
    model = Post
    template_name = 'blog/wpfamily/tag_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(tags__slug__in=[self.kwargs['tag']])

    def get_context_data(self, **kwargs):
        context = super(TagList, self).get_context_data(**kwargs)
        context["tag"] = get_object_or_404(Tag, slug=self.kwargs['tag']).name
        return context


class AuthorList(ListView):
    model = Post
    template_name = 'blog/wpfamily/author_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author__username=self.kwargs['author'])

    def get_context_data(self, **kwargs):
        context = super(AuthorList, self).get_context_data(**kwargs)
        context["author"] = get_object_or_404(User, username=self.kwargs['author']).name
        return context
