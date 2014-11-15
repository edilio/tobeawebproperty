from django.contrib.sitemaps import Sitemap
from django.db.models.loading import get_model
from django.utils import timezone


Career = get_model('web', 'Career')
FAQ = get_model('web', 'FAQ')
ResourceForm = get_model('web', 'ResourceForm')
HelpfulLink = get_model('web', 'HelpfulLink')
Content = get_model('web', 'Content')


class MonthlySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def lastmod(self, obj):
        return timezone.now()


class CareerSitemap(MonthlySitemap):

    def items(self):
        return Career.objects.all()


class FAQSitemap(Sitemap):

    def items(self):
        return FAQ.objects.all()


class ResourceFormSitemap(Sitemap):

    def items(self):
        return ResourceForm.objects.all()


class HelpfulLinkSitemap(Sitemap):

    def items(self):
        return HelpfulLink.objects.all()


class ContentSitemap(Sitemap):

    def items(self):
        return Content.objects.all()


# todo add this models once we have pages designed for them
sitemaps = {
    # 'careers': CareerSitemap,
    # 'faqs': FAQSitemap,
    # 'resources-and-forms': ResourceFormSitemap,
    # 'helpful-links': HelpfulLinkSitemap,
    'pages': ContentSitemap,
}