from django.conf import settings


CONF = getattr(settings, 'REPORTERS', {})
BASE = CONF.get('BASE', 'reporters/report')
URL = CONF.get('URL', 'reporters-report')
