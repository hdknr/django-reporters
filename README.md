# django-reporters

## LOGGING configuration sample

app/loggings.py:

~~~py
HANDLER_CONSOLE = {
    "level": 'DEBUG',
    "class": 'logging.StreamHandler',
}

HANDLER_HTML = {
    'level': 'ERROR',
    'class': 'reporters.handlers.StaticHtmlHandler',
}

LOGGER_DJANGO = {
    'handlers': ['console', 'html'],
    'level': 'INFO',
}

LOGGER_ROOT = {
    'level': 'DEBUG',
    'handlers': ['console'],
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': HANDLER_CONSOLE,
        'html': HANDLER_HTML,
    },
    'loggers': {
        'django': LOGGER_DJANGO,
    },
    'root': LOGGER_ROOT,
}
~~~

app/settings.py:

~~~py
...
if os.path.isfile(os.path.join(BASE_DIR, 'app/loggings.py')):
    from .loggings import *       # NOQA
~~~