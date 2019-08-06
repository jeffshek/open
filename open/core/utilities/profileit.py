import cProfile


def profileit(func):
    """
    Decorator (function wrapper) that profiles a single function
    @profileit()
    def func1(...)
            # do something
        pass
    """

    def wrapper(*args, **kwargs):
        func_name = func.__name__ + ".pfl"
        prof = cProfile.Profile()
        retval = prof.runcall(func, *args, **kwargs)
        prof.dump_stats(func_name)
        return retval

    return wrapper
