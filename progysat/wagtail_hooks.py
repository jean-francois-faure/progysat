from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail_localize.modeladmin.options import TranslatableModelAdmin

from progysat.models.models import Thematic, ActualityType, ResourceType, GeoZone
from progysat.models.news import News
from progysat.models.resource import Resource


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    """Add /static/css/progysat-admin.css to the admin."""
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/progysat-admin.css")
    )


class RessourceModelAdmin(TranslatableModelAdmin):
    model = Resource
    menu_label = "Ressources"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name",)


class ThematicModelAdmin(ModelAdmin):
    model = Thematic
    menu_label = "Thématiques"
    menu_icon = "tag"
    add_to_settings_menu = False
    search_fields = ("name",)


class ResourceTypeModelAdmin(ModelAdmin):
    model = ResourceType
    menu_label = "Types de ressource"
    menu_icon = "tag"
    add_to_settings_menu = False
    search_fields = ("name",)


class RessourcesAdminGroup(ModelAdminGroup):
    menu_label = "Ressources"
    menu_order = 201
    menu_icon = "doc-full"
    items = (RessourceModelAdmin, ThematicModelAdmin, ResourceTypeModelAdmin)


class NewsModelAdmin(TranslatableModelAdmin):
    model = News
    menu_label = "Actualités"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name",)


class ActualityTypeModelAdmin(ModelAdmin):
    model = ActualityType
    menu_label = "Types d'actualité"
    menu_icon = "tag"
    add_to_settings_menu = False
    search_fields = ("name",)


class ActualityAdminGroup(ModelAdminGroup):
    menu_label = "Actualités"
    menu_order = 202
    menu_icon = "date"
    items = (NewsModelAdmin, ActualityTypeModelAdmin)


class GeoZoneModelAdmin(ModelAdmin):
    model = GeoZone
    menu_label = "Zones géographique"
    menu_icon = "site"
    add_to_settings_menu = False
    search_fields = ("name",)


modeladmin_register(RessourcesAdminGroup)
modeladmin_register(ActualityAdminGroup)
modeladmin_register(GeoZoneModelAdmin)
