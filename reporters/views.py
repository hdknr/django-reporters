from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.admin.views.decorators import staff_member_required
from mimetypes import guess_type
from . import conf


@staff_member_required
def report(request, path):
    '''view'''
    path = f'{conf.BASE}/{path}'
    ct, _ = guess_type(path)
    return HttpResponse(
        FileSystemStorage().open(path), content_type=ct)
