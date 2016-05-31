from __future__ import unicode_literals

from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator

from users import models


def class_view_decorator(function_decorator):
    """Convert a function based decorator into a class based decorator usable
    on class based Views.

    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    """

    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator


def profile_required(f):
    def wrapper(request, *args, **kwargs):
        is_filled = bool(request.user.email)

        userinfo = models.UserInfo.objects.get(user=request.user)
        for field in ('nick', 'age', 'phone', 'city', 'med'):
            if not getattr(userinfo, field, None):
                is_filled = False

        if not is_filled:
            return HttpResponse(TemplateResponse(request, 'profile_required.html').render())
        return f(request, *args, **kwargs)
    return wrapper
