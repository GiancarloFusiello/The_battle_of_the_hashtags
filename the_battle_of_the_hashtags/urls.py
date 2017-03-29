from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve

import battles.urls

urlpatterns = [
    url(r'^api/', include(battles.urls)),
    url(r'^admin/', admin.site.urls),
]

if not settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
    ]
