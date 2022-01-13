from django.forms import model_to_dict


def model_to_post_data(model, form_class=None, fields=(), exclude=()):
    if not fields:
        if form_class:
            meta = getattr(form_class, '_meta')
            fields = meta.fields or ()

    if not exclude:
        if form_class:
            meta = getattr(form_class, '_meta')
            exclude = meta.exclude or ()

    if not fields or ('id' not in fields and 'id' not in exclude):
        exclude += ('id',)

    data = model_to_dict(model, fields=fields or None, exclude=exclude or None)
    return data
