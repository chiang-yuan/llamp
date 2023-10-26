

from typing import Any


def _import_mp() -> Any:
    from llamp.utilities.mp import MPAPIWrapper

    return MPAPIWrapper

