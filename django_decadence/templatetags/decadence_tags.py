from django import template
from django.utils.dateparse import parse_datetime
from django_decadence.helpers import check_template_path

register = template.Library()

@register.filter()
def iso_date(value):
    """
    Serialization returns an ISO date by default, this tags
    allows converting it back for displaying it in template
    """
    return parse_datetime(value)


@register.filter()
def serialize(value, user):
    """
    Serialization returns an ISO date by default, this tags
    allows converting it back for displaying it in template
    """
    return value.serialize(user)


@register.simple_tag(takes_context=True)
def decadence_render(context, template_name, data, **kwargs):
    """
    Template tag that renders a template the same way Decadence
    would render it.

    Takes template_name and data in either dict (Decadence serialized)
    or a DecadenceModel
    """
    # validate template path first
    check_template_path(template_name)

    # get template by name
    template_obj = template.loader.get_template(template_name)

    # try to grab request data and user
    user = None
    if hasattr(context, "request"):
        data["request"] = context.request
        user = context.request.user

    # if provided object is not a dict, attempt Decadence serialization
    if not isinstance(data, dict):
        try:
            data = data.serialize(user)
        except AttributeError:
            raise Exception("'%s' is not Decadence-serializable" % type(data))

    # add kwargs to data
    data = {**data, **kwargs}
    return template_obj.render(data)


@register.inclusion_tag("includes/decadence/updatable.html", takes_context=True)
def decadence_updatable(context, path, attrs="", element="span"):
    """
    Generates data-update-group for given path in
    Decadence templates
    """
    update_path = "%(namespace)s-%(obj_id)s-%(path)s" % {
        "namespace": context["update_namespace"],
        "obj_id": context["id"],
        "path": path
    }
    return {
        "path": update_path,
        "value": context[path.split(".")[0]], # ignore users context
        "attrs": attrs,
        "element": element
    }


@register.inclusion_tag("includes/decadence/updatable.html", takes_context=True)
def updatable(context, obj, path, attrs="", element="span"):
    """
    Generates data-update-group for given path in
    Decadence templates
    """
    user = context.request.user
    field = path.split(".")[0] # ignore users context
    value = obj.serialize(user, fields=[field])[field]
    return {
        "path": obj.get_update_path(path),
        "value": value,
        "attrs": attrs,
        "element": element
    }


@register.simple_tag
def value_by_key(obj, key):
    return obj.get(key, "")
