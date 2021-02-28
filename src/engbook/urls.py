from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic.base import RedirectView

def trigger_error(request):
    division_by_zero = 1/0

urlpatterns = [
    # path('', include('landingpage.urls')),
    path('admin/', admin.site.urls),  # The admin route
    path('',  include('user_management.urls')),
    path('',  include('project.urls')),
    path('',  include('log.urls')),
    path('',  include('history.urls')),
    path('gdtbNQsMBVuqfQEhpANtGDxcZwHg/', trigger_error),
    path('jointeam/', RedirectView.as_view(url='http://bit.ly/join-logbook-team'))
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

