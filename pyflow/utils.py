from collections.abc import Callable
from functools import wraps
from pathlib import Path
from time import perf_counter
import chardet
from typing import Any

def timing_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()

        elapsed_time = round(end_time - start_time, 3)
        print(f"{func.__name__} completed in {elapsed_time} seconds")

        return result

    return wrapper


def detect_encoding(file_path: str, sample_size: int = 10000) -> str:
    path = Path(file_path)

    with path.open("rb") as file:
        raw_data = file.read(sample_size)

    result = chardet.detect(raw_data)
    return result.get("encoding") or "utf-8"