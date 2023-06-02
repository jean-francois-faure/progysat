from typing import List

from django.conf import settings
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.documents.models import Document
from wagtail.fields import RichTextField
from wagtail.images.views.serve import generate_image_url
from wagtail.models import Page

from progysat.models.utils import (
    FreeBodyField,
    MultiLanguageTag,
    ModelWithTranslatedName,
)
from progysat.templatetags.main_tags import thematics_page_url


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


class Thematic(MultiLanguageTag):
    class Meta:
        verbose_name = "Thématique"
        verbose_name_plural = "Thématiques"

    image = models.ForeignKey(
        Document,
        verbose_name="Image principale",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    for language_code, _ in settings.LANGUAGES:
        code = language_code.replace("-", "_")
        locals()[f"description_{code}"] = RichTextField(
            verbose_name=f"Description {language_code}",
            max_length=1000,
            default="",
            blank=True,
            null=True,
        )
    color = models.CharField(
        verbose_name="code hex de la couleur (ex 000000 pour du blanc)",
        default="",
        max_length=6,
    )

    @property
    def description(self):
        from django.utils import translation

        return getattr(self, f"description_{translation.get_language()}")

    def to_dict(self):
        if self.image:
            image_link = generate_image_url(self.image, "fill-432x220")
        else:
            image_link = None
        to_return = {
            "name": self.name,
            "description": self.description,
            "slug": self.slug,
            "image": self.image and self.image.url,
            "image_link": image_link,
            "color": self.color,
        }

        return to_return

    @property
    def link(self):
        return thematics_page_url(thematic=self)


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
