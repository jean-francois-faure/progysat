import datetime
from collections import defaultdict
from typing import Dict, Union
from django.conf import settings
from django.utils import translation
from wagtail.templatetags.wagtailcore_tags import pageurl

from progysat.models import ResourcesPage, NewsListPage, Thematic
from progysat.models.models import FooterDetail

DEFAULT_LANGUAGE = settings.LANGUAGES[0][0]
LAST_UPDATE: Dict[str, Union[None, datetime.datetime]] = {
    "general_context": None,
}


def is_recent(key: str):
    """Check if values for the given key have been updated recently."""
    if not LAST_UPDATE[key]:
        return False
    return (datetime.datetime.now() - LAST_UPDATE[key]).total_seconds() < 60  # type: ignore


def update_last_change(key):
    """Mark key as last updated now."""
    LAST_UPDATE[key] = datetime.datetime.now()


def load_general_context(_):
    from wagtail.models import Page, Locale

    language_to_locale_id = {
        locale.language_code: locale.id for locale in Locale.objects.all()
    }
    context_per_language = defaultdict(dict)
    default_locale_id = language_to_locale_id[DEFAULT_LANGUAGE]

    def get_localized_page(page: Page, language: str) -> Page:
        if language == settings.LANGUAGES[0][0]:
            return page
        locale_id = language_to_locale_id[language]
        return Page.objects.filter(
            translation_key=page.translation_key, locale_id=locale_id
        ).first()

    # Add home page
    home_page_in_default_language = Page.objects.filter(
        content_type__model="homepage", locale_id=default_locale_id
    ).first()
    for language_code, _ in language_to_locale_id.items():
        if home_page_in_default_language:
            localized_page = get_localized_page(
                home_page_in_default_language, language_code
            )
            context_per_language[language_code]["home_page"] = localized_page

    # Add resources_link
    resources_page_in_default_language = ResourcesPage.objects.filter(
        locale_id=default_locale_id
    ).first()
    for language_code, _ in language_to_locale_id.items():
        if resources_page_in_default_language:
            localized_page = get_localized_page(
                resources_page_in_default_language, language_code
            )
            context_per_language[language_code]["resources_link"] = pageurl(
                {}, localized_page
            )

    # Add news_list_link
    news_list_page_in_default_language = NewsListPage.objects.filter(
        locale_id=default_locale_id
    ).first()
    for language_code, _ in language_to_locale_id.items():
        if news_list_page_in_default_language:
            localized_page = get_localized_page(
                news_list_page_in_default_language, language_code
            )
            context_per_language[language_code]["news_list_link"] = pageurl(
                {}, localized_page
            )

    # Add bottom footer images
    for language_code, _ in language_to_locale_id.items():
        context_per_language[language_code]["footer_details"] = [
            detail.to_dict(language_code=language_code)
            for detail in FooterDetail.objects.all()
        ]

    return context_per_language


def general_context(_):
    if not is_recent("general_context"):
        update_last_change("general_context")
        general_context._general_context = load_general_context(_)
    language = translation.get_language()
    if (
        getattr(general_context, "_general_context")
        and language in general_context._general_context
    ):
        return general_context._general_context[language]
    return {}


def language(_):
    """Templates need a language_code. Will be overriden by django if defined."""
    from wagtail.models import Locale

    return {
        "language_code": translation.get_language(),
        "language_str": str(Locale.objects.get(language_code="fr")),
    }


def thematics(_):
    return {
        "thematics": Thematic.objects.all(),
    }
