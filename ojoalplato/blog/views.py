# Create your views here.
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import View

from ojoalplato.blog.models import Post


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


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/wpfamily/post_detail.html'


class PostDetailById(View):
    def get(self, request, pk):
        slug = get_object_or_404(Post, id=pk).slug
        return redirect(reverse("post-detail", kwargs={"slug": slug}))


class CategoryList(ListView):
    model = Post
    template_name = 'blog/wpfamily/category_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.category(self.kwargs['category'].lower())

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context["category"] = self.kwargs['category']
        return context
