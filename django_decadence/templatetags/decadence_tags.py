from django import template
from django_decadence.helpers import check_template_path

register = template.Library()

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


@register.simple_tag
def value_by_key(obj, key):
    return obj.get(key, "")
