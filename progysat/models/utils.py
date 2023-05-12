from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


def paragraph_block(additional_field, required):
    return (
        "paragraph",
        blocks.RichTextBlock(
            label="Contenu",
            features=SIMPLE_RICH_TEXT_FIELD_FEATURE
            + ["h3", "h4", "ol", "ul"]
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


class FreeBodyField(models.Model):
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

    body = StreamField(
        [
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
        ],
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
