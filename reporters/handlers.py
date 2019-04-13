from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest
from django.views.debug import ExceptionReporter
from logging import Handler
from copy import copy
from datetime import datetime
from . import signals, utils, conf


class StaticHtmlHandler(Handler):

    def __init__(self):
        Handler.__init__(self)

    def signal(self, request, reporter, name, fullpath):
        try:
            path = reverse(conf.URL, kwargs={'path': name})
        except: 
            path = ''

        if request:
            url = request.build_absolute_uri(path)
        else:
            url = path

        message = utils.render(
            'Exception: {{ exception_type }}:'
            '{% if request %} {{ request.path_info|escape }}\n{% endif %}'
            '{% if exception_value %}{{ exception_value|force_escape }}'
            '{% endif %} <{{ url }}>',
            url=url, **reporter.get_traceback_data())

        signals.report_created.send(
            sender=self.__class__, fullpath=fullpath, message=message)

    def get_filepath(self):
        now = datetime.now()
        day = now.strftime('%Y-%m-%d')
        time = now.strftime('%H-%M-%S')
        return f'{conf.BASE}/{day}/{time}.html'

    def report(self, request, reporter):
        html = reporter.get_traceback_html()
        path = self.get_filepath()
        storage = FileSystemStorage()
        name = storage.save(path, ContentFile(html))
        fullpath = storage.path(name)
        try:
            self.signal(request, reporter, name, fullpath)
        except:
            pass

    def request_error(self, request, *exc_info):
        reporter = ExceptionReporter(request, is_email=False, *exc_info)

        try:
            self.report(request, reporter)
        except:
            pass

    def emit(self, record, *args, **kwargs):
        request = getattr(record, 'request', None)

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        if isinstance(request, WSGIRequest):
            self.request_error(request, *exc_info)
