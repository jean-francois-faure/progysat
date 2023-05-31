from typing import List

from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.documents.models import Document
from wagtail.fields import RichTextField
from wagtail.models import Page

from progysat.models.utils import (
    FreeBodyField,
    MultiLanguageTag,
    ModelWithTranslatedName,
)


class ContentPage(Page, FreeBodyField):
    class Meta:
        verbose_name = "Page de contenu"
        verbose_name_plural = "Pages de contenu"

    subpage_types: List[str] = ["ContentPage"]

    show_in_footer = models.BooleanField(
        verbose_name="Faire apparaître dans le bas de page",
        default=False,
        help_text="Si un lien vers cette page devra apparaître dans le bas de page",
    )

    content_panels = Page.content_panels + FreeBodyField.panels

    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel("show_in_footer"),
            ],
            heading="Pour le bas de page du site",
        ),
    ]


class ResourceType(MultiLanguageTag):
    class Meta:
        verbose_name = "Type de ressource"
        verbose_name_plural = "Types de ressource"


class ActualityType(MultiLanguageTag):
    class Meta:
        verbose_name = "Type d'actualité"
        verbose_name_plural = "Types d'actualité"


class Thematic(MultiLanguageTag):
    class Meta:
        verbose_name = "Thématique"
        verbose_name_plural = "Thématiques"

    image = models.ForeignKey(
        Document, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = RichTextField(max_length=500, default="", blank=True, null=True)

    def to_dict(self):
        to_return = {
            "name": self.name,
            "slug": self.slug,
            "image": self.image and self.image.url,
        }

        return to_return


class GeoZone(MultiLanguageTag):
    class Meta:
        verbose_name = "zone géographique"
        verbose_name_plural = "zones géographiques"

    code = models.CharField(verbose_name="code (ne pas changer !)", max_length=20)
    latitude = models.FloatField(verbose_name="latitude du centre")
    longitude = models.FloatField(verbose_name="longitude du centre")

    icon = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        to_return = {
            "name": self.name,
            "code": self.code,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
        if self.icon:
            to_return["icon"] = self.icon.url
        else:
            to_return["icon"] = f"/static/img/zones/{self.code}.svg"

        return to_return


@register_setting
class StructureSettings(BaseSetting):
    linkedin = models.URLField(
        help_text="URL de votre page LinkedIn", blank=True, null=True
    )

    class Meta:
        verbose_name = "Paramètre de la structure"


@register_setting
class AnalyticsScriptSetting(BaseSetting):
    script = models.TextField(
        help_text="Script d'analytics",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Script de suivi du traffic"


class Contact(models.Model):
    firstname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    subject = models.CharField(max_length=40)
    message = models.TextField()


class FooterDetail(ModelWithTranslatedName):
    class Meta:
        verbose_name = "Image en bas de footer"
        verbose_name_plural = "Images en bas de footer"
        ordering = ("order",)

    image = models.ForeignKey(Document, on_delete=models.CASCADE)
    order = models.FloatField(
        verbose_name="ordre",
        help_text="Les images du bas seront présentées par ordre croissant",
    )
    url = models.URLField(verbose_name="lien", null=True, blank=True)

    def to_dict(self, language_code=None):
        to_return = {"image": self.image.url, "name": self.name, "url": self.url}
        if language_code:
            to_return["name"] = getattr(self, f"name_{language_code.replace('-', '_')}")

        return to_return

    def __str__(self):
        return self.name_fr
