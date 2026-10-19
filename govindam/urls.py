"""
URL configuration for govindam project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

# Import the custom admin site instance
from website.admin import admin_site
from website.sitemaps import StaticViewSitemap, ServiceSitemap, ProductSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'services': ServiceSitemap,
}

urlpatterns = [
    path('admin/', admin_site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('', include('website.urls')),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

