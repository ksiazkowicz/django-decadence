from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def decadence_render(context, template_name, data):
    t = template.loader.get_template(template_name)
    data["request"] = context.request
    return t.render(data)
