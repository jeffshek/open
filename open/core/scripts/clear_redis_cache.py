from django.core.cache import cache


def run():
    # because native django clear cache does not work with django-redis :(
    cache.delete_pattern("*")
