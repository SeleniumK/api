import time
from django.contrib.gis.geos import GEOSGeometry, Point
from functools import wraps

def isiterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True

def to_geom(string):
    """
    Given a string, convert it to a geometry.
    """
    try:
        geom = GEOSGeometry(string)
    except ValueError:
        try:
            lat, lng = [float(coord.strip()) for coord in string.split(',')]
        except ValueError:
            raise ValueError(
                ('Argument must be a comma-separated pair of numbers or a '
                 'string that the GEOSGeometry constructor can handle: %r')
                % string
            )
        else:
            geom = Point(lng, lat)
    return geom

def memo(f):
    """
    A memoization decorator. Borrowed and modified from
    http://code.activestate.com/recipes/576563-cached-property/
    
    You can create a memoized property like:
    
        @property
        @memo
        def attr(self):
            ...
    
    """
    @wraps(f)
    def get(self, *args, **kwargs):
        key = (f, args, tuple(kwargs.items()))
        try:
            return self._method_memos[key]
        except AttributeError:
            self._method_memos = {}
            x = self._method_memos[key] = f(self, *args, **kwargs)
            return x
        except KeyError:
            x = self._method_memos[key] = f(self, *args, **kwargs)
            return x

    return get


def base62_time():
    """
    Convert the current epoch time in milliseconds to a base-64 encoded string.
    """
    ms = int(time.time() * 1000)
    return to_base(ms, 62)


def to_base(num, base):
    """
    Convert an integer to a string in the given base, up to 62.
    """
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    digits = []
    while num > 0:
        num, remainder = divmod(num, base)
        digits.insert(0, alphabet[remainder])

    return ''.join(digits)