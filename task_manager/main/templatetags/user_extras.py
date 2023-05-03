from django import template

register = template.Library()


@register.filter(name='add_classes')
def add_classes(value, arg):
    classes = value.field.widget.attrs.get("class", " ")
    if classes:
        classes = classes.split(' ')
    else:
        classes = []
    new_classes = arg.split(' ')
    for cl in new_classes:
        if cl not in classes:
            classes.append(cl)

    return value.as_widget(attrs={"class": " ".join(classes)})
# | add_classes:'form-group'