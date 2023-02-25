

def filter_nones(body):
    """Filter out keys with values as None
    body - a pydantic schema
    """
    result = {}
    for key in body:
        if body[key] is not None:
            result[key] = body[key]

    return result
