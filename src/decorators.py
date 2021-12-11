import functools
import time
from typing import Callable


def timer(func) -> Callable:
    """Calculate the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        runtime = end_time - start_time
        print(f'Finished in {runtime:.4f}s')
        return result
    return wrapper_timer
