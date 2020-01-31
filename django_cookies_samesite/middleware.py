# Cookie library has moved to http in python3
try:
    import Cookie
except ImportError:
    import http.cookies as Cookie

import warnings

import django

from distutils.version import LooseVersion

from django.conf import settings

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


Cookie.Morsel._reserved['samesite'] = 'SameSite'


class CookiesSameSite(MiddlewareMixin):
    """
    Support for SameSite attribute in Cookies is implemented in Django 2.1 and won't
    be backported to Django 1.11.x.
    This middleware will be obsolete when your app will start using Django 2.1.
    """
    def process_response(self, request, response):

        samesite_flag = getattr(
            settings,
            'SESSION_COOKIE_SAMESITE',
            None
        )

        if not samesite_flag:
            return response

        if samesite_flag.lower() not in {'lax', 'none', 'strict'}:
            raise ValueError('samesite must be "lax", "none", or "strict".')

        for name, cookie in response.cookies.items():
            try:
                response.cookies[name]['samesite'] = samesite_flag.lower()
                response.cookies[name]['secure'] = True
            except:
                pass

        return response
