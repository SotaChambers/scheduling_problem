import time


def stop_watch(f):
    """関数の実行時間を計測するデコレータ"""

    def _stop_watch(*args, **kargs):
        start = time.time()
        result = f(*args, **kargs)
        elapsed_time = time.time() - start
        print(f"{f.__qualname__} took {round(elapsed_time, 3)} seconds")

    return _stop_watch