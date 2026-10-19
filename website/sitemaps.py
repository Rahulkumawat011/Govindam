from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Service, Product

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # List of reverse URL names for active static B2B pages
        return [
            'home', 'about', 'products', 'manufacturing', 'services', 
            'gallery', 'certificates', 'testimonials', 'contact', 
            'privacy_policy', 'terms'
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return Product.objects.filter(status='published')

    def location(self, obj):
        return reverse('product_detail', args=[obj.slug])


class ServiceSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return Service.objects.filter(status='published')

    def location(self, obj):
        return reverse('service_detail', args=[obj.slug])
