import copy
# import cPickle
import _pickle as cPickle


from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, update_last_login
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth import get_backends


def default_dumpped_dict():
    return cPickle.dumps({})

class SSOUser(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=50)
    extras = models.TextField(default=default_dumpped_dict)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __init__(self, *args, **kwargs):
        fieldsOfModel = [x.name for x in self._meta.fields]  # fields can be saved in database

        _kwargs = copy.deepcopy(kwargs)
        extrainfo = {}
        for fn, fv in filter(lambda item: item[0] not in fieldsOfModel, kwargs.items()):
            _kwargs.pop(fn, None)  # only db fields in _kwargs
            extrainfo[fn] = fv
        _kwargs["extras"] = cPickle.dumps(extrainfo)
        return super(SSOUser, self).__init__(*args, **_kwargs)


    def __getattribute__(self, name):
        val = None
        try:  # read from regular field
            val = super(SSOUser, self).__getattribute__(name)
        except AttributeError as e:  # try to read from extra field
            if name.startswith("__"):  # avoid affecting object stuff
                raise e
            try:
                print (name)
                print (self.extras.split("\'")[1].encode())
                val = cPickle.loads(self.extras.split("\'")[1].encode()).get(name)
            except Exception as oe:
                print (oe)
                pass
        return val


@receiver(user_logged_out, sender=SSOUser)
def notify_backend(request, user, *args, **kwargs):
    from authbackend import SSOAuthBackend
    for b in get_backends():
        if isinstance(b, SSOAuthBackend):
            b.storageengine.remove(user.id)

user_logged_in.disconnect(update_last_login)
