from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('', include('landingpage.urls')),
    path('admin/', admin.site.urls),  # The admin route
    path('users/',  include('user_management.urls'))
]


if settings.DEBUG:
    # Add urls for the debug toolbar
    import debug_toolbar
    urlpatterns += [path('__debug__', include(debug_toolbar.urls))]

    # Static and media serving
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
