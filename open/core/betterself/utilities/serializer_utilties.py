def iterable_to_uuids_list(iterable):
    """
    takes an iterable of django objects and gets the str uuid into a list
    """
    result = []
    for item in iterable:
        uuid_label = str(item.uuid)
        result.append(uuid_label)
    return result
