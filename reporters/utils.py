from django.template import Template, Context, loader
from django.core.files.storage import FileSystemStorage
from bs4 import BeautifulSoup as Soup
import os
from . import conf
import re


def render(src, request=None, **kwargs):
    return Template(src).render(Context(kwargs))


def get_storage(*args, **kwargs):
    return FileSystemStorage(*args, **kwargs)


def list_files(*args, **kwargs):
    path = get_storage(*args, **kwargs).path(conf.BASE)
    for (root, _dirs, files) in os.walk(path):
        for filename in files:
            if not filename.endswith('html'):
                continue
            yield os.path.join(root, filename)


def get_storage_path(filename, *args, **kwargs):
    filename = os.path.join(conf.BASE, filename)
    return get_storage(*args, **kwargs).path(filename)


def get_soup(html_stream):
    return Soup(html_stream, "html.parser")


def get_soup_from(filename, *args, **kwargs):
    if not filename.startswith('/'):
        filename = os.path.join(conf.BASE, filename)
    return get_soup(open(filename))


def parse_soup(soup, pattern, selector='.exception_value'):
    src = soup.select(selector)[0].text
    return (re.search(pattern, src), src)
