from django.conf import settings
from django.templatetags.static import static

from progysat.models import HomePage


class SearchDescriptionAndTranslationMiddleware:
    """Middleware to add search_description, seo_title and translated_url to the context."""

    def __init__(self, get_response):
        from wagtail.models import Locale

        self.get_response = get_response
        locales = Locale.objects.all()
        language_to_locale_id = {locale.language_code: locale.id for locale in locales}
        self.home_pages = {
            locale.language_code: HomePage.objects.filter(
                locale=language_to_locale_id[locale.language_code]
            ).first()
            for locale in locales
        }

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        from wagtail.models import Locale

        context = response.context_data

        locales = list(Locale.objects.all())
        translated_urls = {
            locale.language_code: self.home_pages[locale.language_code]
            and self.home_pages[locale.language_code].url
            for locale in locales
        }

        seo_title = None
        search_description = None
        seo_image = static("img/progysat/logo_noir.svg")
        if not context:
            return response
        elif context.get("page"):
            translations = context["page"].get_translations()
            for page_translation in translations:
                translated_urls[
                    page_translation.locale.language_code
                ] = page_translation.url

            seo_title = context["page"].seo_title or context["page"].title
            search_description = context["page"].search_description
            if hasattr(context["page"], "image") and context["page"].image:
                seo_image = context["page"].image.file.url

        # TODO
        # if not search_description:
        #     search_description = getattr(
        #         SeoSettings.for_request(request),
        #         f"search_description_{current_language}",
        #     )

        context["seo_title"] = seo_title
        context["search_description"] = search_description
        context["seo_image"] = settings.WAGTAILADMIN_BASE_URL + seo_image
        context["translated_urls"] = translated_urls
        context["locales"] = locales
        return response
