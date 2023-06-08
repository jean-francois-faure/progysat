from django.conf import settings
from django.db import models
from django.utils import translation
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


def paragraph_block(additional_field, required):
    return (
        "paragraph",
        blocks.RichTextBlock(
            label="Contenu",
            features=SIMPLE_RICH_TEXT_FIELD_FEATURE
            + ["h3", "h4", "ol", "ul", "document-link"]
            + additional_field,
            required=required,
        ),
    )


SIMPLE_RICH_TEXT_FIELD_FEATURE = ["bold", "italic", "link"]
COLOR_CHOICES = (
    ("blue-light", "Bleue"),
    ("secondary-light", "Rose"),
    ("white", "Blanche"),
    ("", "Sans couleur"),
)

color_block = (
    "color",
    blocks.ChoiceBlock(
        label="couleur",
        choices=COLOR_CHOICES,
        default="none",
        help_text="Couleur de fond",
        required=False,
    ),
)
BODY_FIELD_PARAMS = [
    # Is h1
    (
        "heading",
        blocks.CharBlock(form_classname="full title", label="Titre de la page"),
    ),
    (
        "section",
        blocks.StructBlock(
            [
                paragraph_block(["h2"], True),
                color_block,
                (
                    "image",
                    ImageChooserBlock(
                        label="Image à côté du paragraphe", required=False
                    ),
                ),
                (
                    "position",
                    blocks.ChoiceBlock(
                        choices=[
                            ("right", "Droite"),
                            ("left", "Gauche"),
                        ],
                        required=False,
                        help_text="Position de l'image",
                    ),
                ),
                (
                    "sub_section",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                color_block,
                                paragraph_block([], False),
                                (
                                    "columns",
                                    blocks.ListBlock(
                                        blocks.StructBlock(
                                            [
                                                color_block,
                                                paragraph_block([], False),
                                            ],
                                            label="Colonne",
                                        ),
                                        label="Colonnes",
                                    ),
                                ),
                            ],
                            label="Sous section",
                        ),
                        default=[],
                        label="Sous sections",
                    ),
                ),
            ],
            label="Section",
        ),
    ),
    ("image", ImageChooserBlock()),
    ("pdf", DocumentChooserBlock()),
]


class FreeBodyField(models.Model):
    body = StreamField(
        BODY_FIELD_PARAMS,
        blank=True,
        verbose_name="Contenu",
        help_text="Corps de la page",
        use_json_field=True,
    )

    panels = [
        FieldPanel("body", classname="full"),
    ]

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.

    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class ModelWithTranslatedName(models.Model):
    class Meta:
        abstract = True
        ordering = ("name_fr",)

    for language_code, _ in settings.LANGUAGES:
        code = language_code.replace("-", "_")
        locals()[f"name_{code}"] = models.CharField(
            verbose_name=f"Nom {language_code}",
            max_length=100,
            default="",
        )

    @property
    def name(self):
        return getattr(self, f"name_{translation.get_language()}")


class MultiLanguageTag(ModelWithTranslatedName):
    class Meta:
        abstract = True
        ordering = ("name_fr",)

    slug = models.SlugField(
        verbose_name="Slug",
        unique=True,
        max_length=100,
        allow_unicode=True,
        blank=True,
        help_text="ce champ est rempli automatiquement s'il est laissé vide",
    )

    def __str__(self):
        return self.name

    def to_dict(self):
        return {"name": self.name, "slug": self.slug}

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)
