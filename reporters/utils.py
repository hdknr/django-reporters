from django.template import Template, Context, loader
from django.core.files.storage import FileSystemStorage
import os
from . import conf


def render(src, request=None, **kwargs):
    return Template(src).render(Context(kwargs))


def get_storage(*args, **kwargs):
    return FileSystemStorage(*args, **kwargs)


def list_files(*args, **kwargs):
    path = get_storage(*args, **kwargs).path('')
    for (root, _dirs, files) in os.walk(path):
        for filename in files:
            if not filename.endswith('html'):
                continue
            yield os.path.join(root, filename)
