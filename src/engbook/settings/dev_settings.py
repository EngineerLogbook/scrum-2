from .base_settings import *

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
    'djecrety',

]

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Debug Toolbar

# Debug toolbar will only be shown on these IPs
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Add, remove or change the order of panels here.
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

# Add custom toolbar settings here
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_COLLAPSED': False,
}

STATIC_ROOT=""
STATICFILES_DIRS=[
    os.path.join(BASE_DIR, "static")
]
