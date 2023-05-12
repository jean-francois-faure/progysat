from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks
from wagtail.contrib.modeladmin.views import EditView, CreateView

from progysat.models.country import WorldZone, Country
from progysat.models.models import Profile, Thematic, ActualityType, ResourceType
from progysat.models.news import News
from progysat.models.resource import Resource


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    """Add /static/css/progysat-admin.css to the admin."""
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/progysat-admin.css")
    )


class ProfileModelAdmin(ModelAdmin):
    model = Profile
    menu_label = "Profils"
    menu_order = 200
    menu_icon = "group"
    add_to_settings_menu = False
    search_fields = ("name",)


class RelatedCountriesEditView(EditView):
    def dispatch(self, request, *args, **kwargs):
        to_return = super().dispatch(request, *args, **kwargs)
        instance: Resource = self.instance
        instance.add_countries_from_zone()
        return to_return


class RelatedCountriesCreateView(CreateView):
    def dispatch(self, request, *args, **kwargs):
        to_return = super().dispatch(request, *args, **kwargs)
        try:
            instance: Resource = self.get_instance()
            instance.add_countries_from_zone()
        except ValueError:
            pass
        return to_return


class RessourceModelAdmin(ModelAdmin):
    model = Resource
    menu_label = "Ressources"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name",)

    edit_view_class = RelatedCountriesEditView
    create_view_class = RelatedCountriesCreateView


class ThematicModelAdmin(ModelAdmin):
    model = Thematic
    menu_label = "Thématiques"
    menu_icon = "tag"
    add_to_settings_menu = False
    search_fields = ("name",)
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("icon"),
    ]


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


class NewsModelAdmin(ModelAdmin):
    model = News
    menu_label = "Actualités"
    menu_icon = "folder-inverse"
    add_to_settings_menu = False
    search_fields = ("name",)

    edit_view_class = RelatedCountriesEditView
    create_view_class = RelatedCountriesCreateView


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


class WorldZoneModelAdmin(ModelAdmin):
    model = WorldZone
    menu_label = "Zones du monde"
    menu_icon = "site"
    add_to_settings_menu = False
    search_fields = ("name",)


class CountryModelAdmin(ModelAdmin):
    model = Country
    menu_label = "Pays"
    menu_icon = "site"
    add_to_settings_menu = False
    search_fields = ("name",)


class GeneralAdminGroup(ModelAdminGroup):
    menu_label = "Général"
    menu_order = 203
    menu_icon = "cogs"
    items = (ProfileModelAdmin, CountryModelAdmin, WorldZoneModelAdmin)


modeladmin_register(RessourcesAdminGroup)
modeladmin_register(ActualityAdminGroup)
modeladmin_register(GeneralAdminGroup)
