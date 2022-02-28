from django import template

register = template.Library()


@register.filter(name='add_attr')
def add_attribute(field, css):
    attrs = field.subwidgets[0].data['attrs']
    definition = css.split(',')

    for d in definition:
        key, val = d.split(':')
        if key:
            if key in attrs:
                attrs[key] += f" {val}"
            else:
                attrs[key] = val

    return field.as_widget(attrs=attrs)


@register.filter(name='add_str')
def add_string(arg1, arg2):
    if not arg2:
        arg2 = ""
    return str(arg1) + str(arg2)


@register.filter('field_type')
def field_type(field):
    return field.field.widget.__class__.__name__
