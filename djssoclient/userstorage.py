# import cPickle
import _pickle as cPickle
from . import SSO_SETTING_CACHE
# from django.core.cache import get_cache
from django.core import signals
from .models import SSOUser


def get_cache(backend, **kwargs):
    """
    Compatibilty wrapper for getting Django's cache backend instance
    """
    try:
        from django.core.cache import _create_cache
    except ImportError:
        # Django < 1.7
        from django.core.cache import get_cache as _get_cache
        return _get_cache(backend, **kwargs)

    cache = _create_cache(backend, **kwargs)
    # Some caches -- python-memcached in particular -- need to do a cleanup at the
    # end of a request cycle. If not implemented in a particular backend
    # cache.close is a no-op
    signals.request_finished.connect(cache.close)
    return cache

class SSOUserStorage(object):
    class Meta:
        abstract = True

    def save(self, userid, ssouser):
        raise NotImplementedError()

    def find(self, userid):
        raise NotImplementedError()

    def remove(self, userid):
        raise NotImplementedError()


class SSOUserCacheStorage(SSOUserStorage):
    def __init__(self):
        self.cache = get_cache(SSO_SETTING_CACHE)

    def _get_cached_id(self, userid):
        return "sso_user_%s" % userid

    def save(self, userid, ssouser):
        self.cache.set(self._get_cached_id(userid),
                       cPickle.dumps(ssouser), timeout=None)

    def find(self, userid):
        return cPickle.loads(self.cache.get(self._get_cached_id(userid)))

    def remove(self, userid):
        self.cache.delete(self._get_cached_id(userid))


class SSOUserDBStorage(SSOUserStorage):
    def save(self, userid, ssouser):
        ssouser.save()

    def find(self, userid):
        return SSOUser.objects.get(pk=userid)

    def remove(self, userid):
        try:
            SSOUser.objects.get(pk=userid).delete()
        except:
            pass
