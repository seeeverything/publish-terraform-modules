def str_to_bool(value: str, default: bool = False) -> bool:
    if value.lower() in ["true"]:
        return True
    elif value.lower() in ["false"]:
        return False
    return default
