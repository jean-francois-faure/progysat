from django.contrib.auth.models import User
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class HomePage(Page, models.Model):
    from progysat.models.utils import SIMPLE_RICH_TEXT_FIELD_FEATURE

    def get_context(self, request, *args, **kwargs):
        from progysat.models.resource import Resource
        from progysat.models.models import Profile
        from progysat.models.news import News

        context = super().get_context(request, *args, **kwargs)
        context["n_resources"] = Resource.objects.count()
        context["n_members"] = User.objects.count()
        context["profiles"] = Profile.objects.all()
        first_news = News.objects.filter(is_progysat=True).first()
        if not first_news:
            first_news = News.objects.filter().first()
        if first_news:
            news_list = [first_news] + list(News.objects.exclude(id=first_news.id)[:2])
        else:
            news_list = News.objects.all()[:3]
        context["news_list"] = news_list
        return context

    # HomePage can be created only on the root
    parent_page_types = ["wagtailcore.Page"]

    introduction = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Introduction",
    )
    resources_block_title = models.CharField(
        blank=True,
        verbose_name="Titre du bloc des ressources",
        max_length=64,
        default="Des ressources adaptées à votre profil",
    )
    resources_block_explication = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Explication du bloc des ressources",
        help_text="Explication présente sous les listes des différents profils",
    )
    news_block_title = models.CharField(
        blank=True,
        verbose_name="Titre du bloc des actualités",
        max_length=64,
        default="Dernières actualités",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("resources_block_title"),
        FieldPanel("resources_block_explication"),
        FieldPanel("news_block_title"),
    ]

    class Meta:
        verbose_name = "Page d'accueil"
