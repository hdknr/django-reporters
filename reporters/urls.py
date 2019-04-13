from django.urls import re_path
from . import views, conf


urlpatterns = [
    re_path('report/(?P<path>.*)', views.report, name=conf.URL),
]
