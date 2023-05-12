from typing import List

from django.db import models
from django.templatetags.static import static
from taggit.models import TagBase
from unidecode import unidecode
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.core.templatetags.wagtailcore_tags import pageurl
from wagtail.documents.models import Document

from progysat.models.utils import FreeBodyField, SIMPLE_RICH_TEXT_FIELD_FEATURE


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


class ResourceType(TagBase):
    class Meta:
        ordering = ("name",)
        verbose_name = "Type de ressource"
        verbose_name_plural = "Types de ressource"


class ActualityType(TagBase):
    class Meta:
        ordering = ("name",)
        verbose_name = "Type d'actualité"
        verbose_name_plural = "Types d'actualité"


class Profile(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Description",
    )
    types = models.ManyToManyField(ResourceType, verbose_name="types de ressource")

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("types"),
    ]

    def __str__(self):
        return self.name

    @property
    def icon_url(self):
        return static(f"img/{self.slug}.svg")

    @property
    def slug(self):
        return unidecode(self.name.lower())

    @property
    def resources_link(self):
        from progysat.models.resources_page import ResourcesPage

        return f"{pageurl({}, ResourcesPage.objects.get())}?profile={self.slug}"

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"


class Thematic(TagBase):
    class Meta:
        verbose_name = "Thématique"
        verbose_name_plural = "Thématiques"

    icon = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def icon_or_default(self):
        if self.icon:
            return self.icon.url
        else:
            return f"/static/img/thematics/{self.slug}.svg"

    def to_dict(self):
        to_return = {"name": self.name, "slug": self.slug, "icon": self.icon_or_default}

        return to_return


@register_setting
class StructureSettings(BaseSetting):
    linkedin = models.URLField(
        help_text="URL de votre page LinkedIn", blank=True, null=True
    )

    class Meta:
        verbose_name = "Paramètre de la structure"


@register_setting
class NewsLetterSettings(BaseSetting):
    newsLetter = models.URLField(
        help_text="Lien d'inscription à la lettre d'information",
        max_length=300,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Inscription à la lettre d'information"


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
