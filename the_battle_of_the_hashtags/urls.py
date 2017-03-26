from django.conf.urls import url, include
from django.contrib import admin

import battles.urls

urlpatterns = [
    url(r'^api/', include(battles.urls)),
    url(r'^admin/', admin.site.urls),
]
