from django.core.cache import cache

"""
dpy runscript clear_redis_cache
"""


def run():
    # because native django clear cache does not work with django-redis :(
    cache.delete_pattern("*")
