from django.utils import translation 
import djclick as click
from logging import getLogger
from reporters import utils
from bs4 import BeautifulSoup as Soup
import os
import re
import json


logger = getLogger()
translation.activate('ja')


@click.group(invoke_without_command=True)
@click.option('--location', '-l', default=None, 
              help="parent directory of the conf.BASE(MEDIA_ROOT)")
@click.pass_context
def main(ctx, location):
    # print(type(ctx), dir(ctx))
    ctx.obj = {'location': location}


IGNORES = [
    "^Invalid HTTP_HOST header:.+'(?P<host>[^']+)'.",
    "^\[Errno 2\] No such file or directory:.+'(?P<path>[^']+)'",
]

@main.command()
@click.argument('filename')
@click.option('--delete', '-d', is_flag=True)
@click.pass_context
def can_ignore(ctx, filename, delete):
    '''Check if can be ignored'''

    def _report(path, pattern, ma, do_delete):
        params = {
            "path": path,
            "pattern": pattern,
            "params": ma.groupdict(),
        }
        click.echo(json.dumps(params,indent=2))
        if do_delete:
            os.remove(path)

    def _do(path):
        soup = utils.get_soup_from(path)
        for pattern in IGNORES:
            ma, text = utils.parse_soup(soup, pattern)
            if ma:
                _report(path, pattern, ma, delete)

    if filename == 'all':
        for path in utils.list_files(location=ctx.obj['location']):
            _do(path)
        return

    _do(utils.get_storage_path(filename, location=ctx.obj['location']))
