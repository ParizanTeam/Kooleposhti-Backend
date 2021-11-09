def get_attr(obj, attr_name):
    """
    Get attribute from object
    :param obj: object
    """
    attrs = []
    for attr in dir(obj):
        if attr_name in attr:
            attrs.append(attr)
    return attrs
