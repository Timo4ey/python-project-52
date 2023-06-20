from django import template

register = template.Library()


@register.filter(name="add_classes")
def add_classes(value, arg):
    classes = value.field.widget.attrs.get("class", " ")
    if classes:
        classes = classes.split(" ")
    else:
        classes = []
    new_classes = arg.split(" ")
    for cl in new_classes:
        if cl not in classes:
            classes.append(cl)

    return value.as_widget(attrs={"class": " ".join(classes)})


@register.filter(name="delete_id")
def delete_id(value):
    print(value.field.widget.attrs)
    item_id = value.field.widget.attrs.get("id", " ")
    if item_id:
        # item_id = item_id.split(' ')
        print(item_id)
    else:
        # item_id = []
        print("no")
