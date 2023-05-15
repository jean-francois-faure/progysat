from bs4 import BeautifulSoup
from django import forms
from django.db import models
from django.forms import model_to_dict
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.search import index

from progysat.models.country import Country, WorldZone
from progysat.models.models import Thematic, Profile, ResourceType
from progysat.models.utils import (
    TimeStampedModel,
    SIMPLE_RICH_TEXT_FIELD_FEATURE,
    FreeBodyField,
)


class Resource(index.Indexed, TimeStampedModel, FreeBodyField):
    countries = models.ManyToManyField(Country, verbose_name="Pays", blank=True)
    zones = models.ManyToManyField(WorldZone, verbose_name="Zones", blank=True)
    is_global = models.BooleanField(
        verbose_name="Concerne tous les pays", default=False
    )
    name = models.CharField(verbose_name="Nom", max_length=100)
    slug = models.SlugField(
        max_length=100,
        verbose_name="Slug (URL de la ressource)",
        unique=True,
        blank=True,
        default="",
        help_text="ce champ est rempli automatiquement s'il est laissé vide",
    )
    thematics = models.ManyToManyField(
        Thematic, blank=True, verbose_name="Thématiques", related_name="ressources"
    )
    main_thematic = models.ForeignKey(
        Thematic,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Thématique principale",
        help_text="ce champ n'est utilisé que lorsque plusieurs thématiques sont sélectionnées",
    )
    profiles = models.ManyToManyField(
        Profile, blank=True, verbose_name="Profils", related_name="ressources"
    )
    geo_dev_creation = models.BooleanField(
        default=False, verbose_name="Créé par Progysat ?"
    )
    source_name = models.CharField(
        verbose_name="Producteur de la ressource", max_length=100, blank=True
    )
    source_link = models.CharField(
        verbose_name="Lien vers la Ressource (URL)", max_length=200, blank=True
    )
    file = models.FileField(
        verbose_name="Fichier source",
        blank=True,
        null=True,
        help_text="S'il est défini, le lien vers la source est ignoré",
    )
    short_description = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Description courte",
        max_length=1000,
    )
    types = models.ManyToManyField(ResourceType, blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("short_description"),
        FieldPanel("source_name"),
        FieldPanel("source_link"),
        FieldPanel("file"),
        FieldPanel("body"),
        FieldPanel("types", widget=forms.CheckboxSelectMultiple),
        FieldPanel("thematics", widget=forms.CheckboxSelectMultiple),
        FieldPanel("profiles", widget=forms.CheckboxSelectMultiple),
        FieldPanel("geo_dev_creation"),
        FieldPanel("is_global"),
        FieldPanel("zones", widget=forms.CheckboxSelectMultiple),
        FieldPanel("countries", widget=forms.SelectMultiple),
    ]

    def to_dict(self):
        to_return = model_to_dict(
            self,
            fields=[
                "id",
                "is_global",
                "name",
                "slug",
                "thematics",
                "profiles__name",
                "geo_dev_creation",
                "source_name",
                "short_description",
            ],
        )
        to_return["profiles"] = [profile.slug for profile in self.profiles.all()]
        to_return["thematics"] = [thematic.slug for thematic in self.thematics.all()]
        to_return["is_description_long"] = (
            is_description_long := len(self.short_description) >= 250
        )
        to_return["short_description_max_250"] = self.short_description[:250]
        if is_description_long:
            to_return["short_description_max_250"] += "..."
        if len(to_return["thematics"]) == 1:
            to_return["thematic"] = to_return["thematics"][0]
        elif len(to_return["thematics"]) > 1 and self.main_thematic:
            to_return["thematic"] = self.main_thematic.slug
        else:
            to_return["thematic"] = "multiple"
        zones = {country.zone.code for country in self.countries.all() if country.zone}
        if len(zones) == 1:
            to_return["zone"] = next(iter(zones))
        else:
            to_return["zone"] = None
        to_return["link"] = self.link
        if self.file:
            to_return["download_name"] = self.file.name
        else:
            to_return["download_name"] = None
        to_return["is_download"] = self.is_download
        to_return["countries"] = [country.code for country in self.countries.all()]
        to_return["types"] = [type_.slug for type_ in self.types.all()]
        return to_return

    def __str__(self):
        return self.name

    def get_main_thematic(self):
        if self.main_thematic:
            return self.main_thematic
        if self.thematics.count() == 1:
            return self.thematics.first()
        return None

    def add_countries_from_zone(self):
        # add all countries of all selected zones
        for zone in self.zones.all():
            for country in zone.country_set.all():
                self.countries.add(country)
        super().save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def link(self):
        if self.file:
            return self.file.url
        if self.source_link:
            return self.source_link

    @property
    def is_download(self):
        return bool(self.file)

    @property
    def description_text(self):
        return BeautifulSoup(self.short_description, "html.parser").text

    class Meta:
        verbose_name_plural = "Ressources"
        verbose_name = "Ressource"
        ordering = ("name",)
