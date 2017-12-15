# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.template import Context, loader
from django.views.generic import ListView
from django_decadence.models import SerializableQuerySet


class DecadenceListView(ListView):
    """
    Custom ListView that adds "serialized" to context with Decadence-serialized queryset
    """
    def get(self, request, *args, **kwargs):
        original = super(DecadenceListView, self).get(request, *args, **kwargs)
        if request.is_ajax():
            context = self.get_context_data()
            data = {
                "results": context.get("serialized", []),
                "page": 1,
                "is_paginated": context.get("is_paginated", False),
                "range": [1, ],
                "count": self.object_list.count(),
                "num_pages": 1,
            }

            # include pagination data if available
            page = context.get("page_obj", None)
            if page:
                data["page"] = page.number
                data["num_pages"] = page.paginator.num_pages
                data["range"] = list(page.paginator.page_range)

            return JsonResponse(data)
        else:
            return original

    def get_context_data(self):
        context = super(DecadenceListView, self).get_context_data()
        original_list = context["object_list"]
        context["serialized"] = original_list.serialized(self.request.user) if original_list else None
        return context


class DecadenceTableView(DecadenceListView):
    """
    Implements a Decadence-serialized paginated table view.
    """
    def get_context_data(self):
        context = super(DecadenceTableView, self).get_context_data()
        context["table_model"] = self.table_model
        try:
            context["update_namespace"] = self.model.updates_namespace
        except:
            pass
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
