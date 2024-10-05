from typing import Any

class SingletonMeta(type):
    _instances: dict[type, object] = {}

    def __call__(cls, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
