def vals(obj):
    if hasattr(obj, "__dict__"):
        return {arg: vars(obj)[arg] for arg in vars(obj)}

    if hasattr(obj, "__slots__"):
        return {arg: obj.__getattribute__(arg) for arg in obj.__slots__}

    return obj