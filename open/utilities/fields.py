from django.db.models import CharField

# simplify charfield because i always have to think what to put for these parameters
# whereas it's almost always the same/similar to below
DEFAULT_MODELS_CHAR_FIELD = CharField(
    max_length=300, blank=False, default="", null=False
)


def create_django_choice_tuple_from_list(list_a):
    if list_a is None:
        return ()

    tuples_list = []
    for item in list_a:
        if isinstance(item, str):
            tuple_item_title = item.title()
        else:
            tuple_item_title = item

        tuple_item = (item, tuple_item_title)
        tuples_list.append(tuple_item)

    return tuple(tuples_list)
