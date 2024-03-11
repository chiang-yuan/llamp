from typing import Any


def _import_mp() -> Any:
    from llamp.utilities.mp import MPAPIWrapper

    return MPAPIWrapper


def __getattr__(name: str) -> Any:
    if name == "MPAPIWrapper":
        return _import_mp()
    else:
        raise AttributeError(f"Could not find: {name}")


__all__ = [
    "MPAPIWrapper",
]
