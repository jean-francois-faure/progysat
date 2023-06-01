from typing import List

from django.http import Http404
from django.utils import translation
from rest_framework.utils import json
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.models import Page

from progysat.models import Thematic
from progysat.models.news import News


class ThematicsListPage(RoutablePageMixin, Page):
    class Meta:
        verbose_name = "Page des thématiques"
        verbose_name_plural = "Pages des thématiques"

    parent_page_types = ["progysat.HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    @route(r"^(.*)/$", name="thematic")
    def access_thematics_page(self, request, thematics_slug):
        try:
            thematic = Thematic.objects.get(slug=thematics_slug)
        except (News.DoesNotExist, News.MultipleObjectsReturned):
            raise Http404

        return self.render(
            request,
            context_overrides={
                "thematic": thematic,
                "thematics_page": ThematicsListPage.for_current_language(),
            },
            template="progysat/thematic_page.html",
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["thematics_list"] = json.dumps(
            [thematic.to_dict() for thematic in Thematic.objects.all()]
        )

        return context

    @staticmethod
    def for_current_language():
        current_language = translation.get_language()
        return ThematicsListPage.objects.get(locale__language_code=current_language)
