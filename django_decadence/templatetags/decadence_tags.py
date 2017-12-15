from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def decadence_render(context, template_name, data):
    t = template.loader.get_template(template_name)
    try:
        data["request"] = context.request
    except:
        pass
    return t.render(data)


@register.simple_tag
def value_by_key(obj, key):
    return obj.get(key, "")
