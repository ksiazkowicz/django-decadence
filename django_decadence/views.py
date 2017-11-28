# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.http import HttpResponse, HttpResponseServerError
from django.template import Context, loader
from django.views.generic import ListView
from django_decadence.models import SerializableQuerySet


class DecadenceListView(ListView):
    """
    Custom ListView that adds "serialized" to context with Decadence-serialized queryset
    """
    def get_context_data(self):
        context = super(DecadenceListView, self).get_context_data()
        original_list = context["object_list"]
        context["serialized"] = original_list.serialized(self.request.user) if original_list else None
        return context


def generate_html(request):
    """
    Generates HTML code from request. You should send a JSON through post this way:
    csrfmiddlewaretoken=token&data={"template": "includes/decadence/cancer.html", ...}
    Data should have a template + context.
    """
    # get request data from JSON first
    request_data = request.POST.get("data", "{}")
    # parse as JSON
    request_data = json.loads(request_data)

    # get template file path
    template_file = request_data.get("template", "")

    # check if path is valid
    if not template_file.startswith("includes/decadence/"):
        return HttpResponseServerError("<h1>Invalid template</h1>")

    # load the template and render it
    t = loader.get_template(template_file)
    rendered = t.render(request_data, request)

    return HttpResponse(rendered, content_type="text/html")
