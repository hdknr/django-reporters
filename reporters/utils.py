from django.template import Template, Context, loader


def render(src, request=None, **kwargs):
    return Template(src).render(Context(kwargs))
