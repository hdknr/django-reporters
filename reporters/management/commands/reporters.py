from django.utils import translation 
import djclick as click
from logging import getLogger
from reporters import utils
from bs4 import BeautifulSoup as Soup
import os
import re


logger = getLogger()
translation.activate('ja')


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    pass


def check_invalid_host_header(value, soup):
    match = re.search("^Invalid HTTP_HOST header:.+'(?P<host>[^']+)'.", value)
    return match


@main.command()
@click.option('--base', '-b', default=None)
@click.pass_context
def delete_invalid_host_header(ctx, base):
    '''List Files'''
    for path in utils.list_files(location=base):
        soup = Soup(open(path), "html.parser")
        exception_value = soup.select('.exception_value')[0].text
        match = check_invalid_host_header(exception_value, soup)
        if match:
            click.echo(match.groupdict()['host'])
            os.remove(path)
