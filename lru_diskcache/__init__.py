import functools
import pickle
import gzip
from pathlib import Path

from lru_diskcache.ordered_dict_storage import OrderedDictStorage


def lru_diskcache(maxsize=16):
    """
    This creates a decorator, which caches pair of arguments and return value of the decorated function.
    The key value pair is stored to local folder cashe_of_ + name of the funtcion.
    The arguments and functions are serialized to pickle files.

    Parameters
    ----------
    maxsize - maximum number of stored results

    Returns
    -------

    Examples
    --------
    >>> import random
    >>> @lru_diskcache(maxsize=32)
    ... def function(a, b=10):
    ...     return random.randint(0, 100)

    >>> function(10)
    32
    >>> function(11)
    55
    >>> function(10)
    32

    """

    def lru_diskcache_inner(func):
        directory = Path("cashe_of_" + func.__name__)
        if not directory.is_dir():
            directory.mkdir()

        key_dequeue_file = directory.joinpath("cache_table.json")
        key_dequeue = OrderedDictStorage(file=key_dequeue_file)

        @functools.wraps(func)
        def cache_result(*args, **kwargs):
            key = repr(args) + repr(kwargs)
            if key in key_dequeue:
                filename = key_dequeue[key]
                cache_file = Path(filename)
            else:
                filename = str(abs(hash(key))) + ".pickle.gz"
                cache_file = directory.joinpath(filename)

            if cache_file.exists():
                with gzip.open(cache_file) as f:
                    return pickle.load(f)

            result = func(*args, **kwargs)

            if len(key_dequeue) >= maxsize:
                key_to_remove, file_to_remove = key_dequeue.popitem(last=False)
                Path(file_to_remove).unlink()

            key_dequeue[key] = str(cache_file)

            with gzip.open(cache_file, 'w') as f:
                pickle.dump(result, f)

            key_dequeue.save()

            return result

        return cache_result
    return lru_diskcache_inner
