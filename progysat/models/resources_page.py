import json
from typing import List

from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.models import Page

from progysat.models import Resource
from progysat.models.models import ResourceType, GeoZone, Thematic
from progysat.utils import objects_for_current_language


class ResourcesPage(RoutablePageMixin, Page):
    class Meta:
        verbose_name = "Page des ressources"
        verbose_name_plural = "Pages des ressources"

    parent_page_types = ["progysat.HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["has_vue"] = True
        context["thematics"] = json.dumps(
            [thematic.to_dict() for thematic in Thematic.objects.all()]
        )
        context["resource_types"] = json.dumps(
            [type_.to_dict() for type_ in ResourceType.objects.all()]
        )
        context["zones"] = json.dumps(
            [zone.to_dict() for zone in GeoZone.objects.all()]
        )
        context["resources"] = json.dumps(
            [
                ressource.to_dict()
                for ressource in objects_for_current_language(Resource)
            ]
        )
        return context
