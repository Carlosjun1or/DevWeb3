from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def admin_required(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_admin(request.user):
            raise PermissionDenied('Você não tem permissão para acessar esta área.')
        return view_func(request, *args, **kwargs)

    return _wrapped_view
