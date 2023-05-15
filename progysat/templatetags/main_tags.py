import hashlib

from django.template.defaulttags import register


@register.simple_tag()
def news_page_url(news=None):
    from progysat.models.news_list_page import NewsListPage

    try:
        news_list_page = NewsListPage.objects.get()
    except NewsListPage.DoesNotExist:
        raise NewsListPage.DoesNotExist("A NewsListPage must be created")

    if news is None:
        return news_list_page.url
    url = news_list_page.url + news_list_page.reverse_subpage(
        "news",
        args=(str(news.slug),),
    )
    return url


@register.simple_tag()
def image_id_from_url(image_url):
    hash_ = hashlib.md5()
    hash_.update(image_url.encode("utf8"))
    return str(int(hash_.hexdigest(), 16))[0:12]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
