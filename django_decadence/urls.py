from django.conf.urls import url
from django_decadence.views import generate_html

urlpatterns = [
    url(r'^template/$', generate_html, name='decadence_template'),
]