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


@register.simple_tag()
def updatable_new(obj, path, value=None):
    """
    Simple templatetag for including specific span element with a proper 
    data-update-group data attribute, that enables Updates API.

    :param obj: instance of DecadenceModel
    :param path: path which defines specific element to update (ex. like.23)
    :param value: current value of this element (ex. 5)

    Returns:
        .. code-block:: html
        
            <span data-update-group='post-12-like.23'>5</span>
    """
    return template.Template("<span data-update-group='{{ path }}'>{{ value }}</span>").render(template.Context({
        "path": obj.get_update_path(path),
        "value": value
    }))


@register.simple_tag()
def updatable(namespace, obj, path, value=""):
    """
    Simple templatetag for including specific span element with a proper 
    data-update-group data attribute, that enables Updates API.

    :param namespace: update namespace, for example model name (ex. post)
    :param obj: object id (ex. 12)
    :param path: path which defines specific element to update (ex. like.23)
    :param value: current value of this element (ex. 5)

    Returns:
        .. code-block:: html
        
            <span data-update-group='post-12-like.23'>5</span>
    """
    return template.Template("<span data-update-group='{{ namespace }}-{{ object }}-{{ path }}'>{{ value }}</span>").render(template.Context({
        "namespace": namespace,
        "object": obj,
        "path": path, 
        "value": value
    }))


@register.simple_tag
def value_by_key(obj, key):
    return obj.get(key, "")
