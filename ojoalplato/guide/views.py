from django.views.generic import DetailView

from ojoalplato.guide.models import Guide


class GuideDetailView(DetailView):
    model = Guide
    template_name = "guide/guide_detail.html"
    context_object_name = "guide"
