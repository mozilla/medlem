from django.views import static
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin


# import medlem.base.urls
import medlem.api.urls


urlpatterns = [
    url(
        r'^api/v1/',
        include(medlem.api.urls, namespace='api')
    ),

    url(
        r'^admin/',
        include(admin.site.urls)
    ),

    # contribute.json url
    url(r'^(?P<path>contribute\.json)$',
        static.serve,
        {'document_root': settings.ROOT},
    ),
]
