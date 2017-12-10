# Create your views here.
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic import View
from django.db.models import Count

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
        return Post.objects.published().order_by("-post_date")

    def get(self, request, **kwargs):
        if request.GET.get("p"):
            post_id = request.GET.get("p")
            slug = get_object_or_404(Post, id=post_id).slug
            return redirect(reverse("post-detail", kwargs={"slug": slug}), permanent=True)
        else:
            return super(ListView, self).get(request, **kwargs)


class PostDetail(HitCountDetailView):
    model = Post
    template_name = 'blog/wpfamily/post_detail.html'
    count_hit = True


class PostDetailById(View):
    def get(self, request, pk):
        slug = get_object_or_404(Post, id=pk).slug
        return redirect(reverse("post-detail", kwargs={"slug": slug}), permanent=True)


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


class CategoriesList(ListView):
    model = Category
    template_name = 'blog/wpfamily/categories_list.html'

    def get_queryset(self):
        return Category.objects.filter(active=True).annotate(num_posts=Count("post")).order_by("-num_posts")


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


class TagsList(ListView):
    model = Tag
    template_name = 'blog/wpfamily/tags_list.html'

    def get_queryset(self):
        return Tag.objects.all().annotate(num_posts=Count("post")).order_by("-num_posts")


class CategoriesAndTagsView(ListView):
    template_name = 'blog/wpfamily/more_list.html'
    context_object_name = 'categories_list'
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoriesAndTagsView, self).get_context_data(**kwargs)
        context.update({
            'tags_list': Tag.objects.all().annotate(num_posts=Count("post")).order_by("-num_posts")
        })
        return context

    def get_queryset(self):
        return Category.objects.filter(active=True).annotate(num_posts=Count("post")).order_by("-num_posts")


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
