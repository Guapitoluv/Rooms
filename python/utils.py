import json

def is_json_serializable(obj) -> bool:
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False