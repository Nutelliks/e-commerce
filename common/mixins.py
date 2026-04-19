from django.core.cache import cache


class CacheMixin:
    def get_set_cache(self, cache_name, timeout, builder):
        data = cache.get(cache_name)

        if data is None:
            data = builder()
            cache.set(cache_name, data, timeout)

        return data