from django.db.models.fields.related import ManyToManyField

def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)
    return data


def get_deep_attr(model, field):
    """
    this is a static moethod to get forigen keys or OneToOne fields in model fiends
    similar to get_attr
    :param model:
    :param field: use __ for foreign key field, eg user__username
    :return:
    """

    def get_repr(value):
        if callable(value):
            return '%s' % value()
        return value

    def get_field(instance, field):
        field_path = field.split('__')
        attr = instance
        for elem in field_path:
            try:
                attr = getattr(attr, elem)
            except AttributeError:
                return None
        return attr

    return get_repr(get_field(model, field))