from bs4 import BeautifulSoup
from django.contrib.syndication.views import Feed
from django.utils import translation

from progysat.models.news import News
from progysat.templatetags.main_tags import news_page_url


class LatestNewsFeed(Feed):
    title = "News"
    link = "/feed/news/latest"
    description = "Les dernières actualités de Progysat."
    description_template = "rss_feed.html"

    @staticmethod
    def prepare_item(news: News):
        news.introduction = BeautifulSoup(news.introduction, "html.parser").text
        return news

    def item_pubdate(self, item: News):
        return item.publication_date

    def items(self):
        return [
            self.prepare_item(news)
            for news in News.objects.filter(
            locale__language_code=translation.get_language()
        ).order_by("-publication_date")[:5]
        ]

    def item_title(self, item):
        return item.name

    def item_link(self, item):
        return news_page_url(item)

    def get_context_data(self, **kwargs):
        """
        {'obj': item, 'site': current_site} as the super context.
        """
        context = super().get_context_data(**kwargs)
        context["image_url"] = (
            context["site"].domain + context["obj"].image.file.url
            if context["obj"].image
            else None
        )
        return context
