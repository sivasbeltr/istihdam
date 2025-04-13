"""
URL configuration for istihdam project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Ana sayfa
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # Diğer URL yapısı için yertutucu
    path(
        "hakkimizda/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path(
        "iletisim/",
        TemplateView.as_view(template_name="pages/contact.html"),
        name="contact",
    ),
    path(
        "firmalar/",
        TemplateView.as_view(template_name="firmalar/list.html"),
        name="firmalar",
    ),
    path(
        "ustalar/",
        TemplateView.as_view(template_name="ustalar/list.html"),
        name="ustalar",
    ),
    path(
        "ilanlar/",
        TemplateView.as_view(template_name="ilanlar/list.html"),
        name="ilanlar",
    ),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
