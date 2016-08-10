# Create your views here.
from django.views.generic import ListView

from ojoalplato.blog.models import Post


class PostList(ListView):
    model = Post
    template_name = 'blog/wpfamily/home.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status="publish")

