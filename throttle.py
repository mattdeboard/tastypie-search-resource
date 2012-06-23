from django.conf import settings

from tastypie.throttle import CacheDBThrottle


class SmartCacheDBThrottle(CacheDBThrottle):
    """
    Custom throttling class to address bug in Tastypie that manifests
    when trying to run tests or do any kind of development with a Resource
    that has some kind of throttling configured. Tastypie is not smart
    about checking whether or not DummyCache is being used, so we'll use
    this to make it be smart.

    Requires Django 1.3+.
    
    """
    def should_be_throttled(self, identifier, **kwargs):
        # Tastypie barfs if you try to do anything with throttling when using
        # a dummy cache. In production this isn't a big deal, but in a dev
        # environment this is a huge PITA. Check the cache type, and if we ARE
        # using dummy cache, just act like we did a cache check and didn't find
        # the key.
        cache = getattr(settings, 'CACHES', {})
        cache_default = cache.get('default')
        
        if cache_default and cache_default['BACKEND'].endswith('DummyCache'):
            return False
        else:
            return (super(SmartCacheDBThrottle, self)\
                    .should_be_throttled(identifier, **kwargs))


