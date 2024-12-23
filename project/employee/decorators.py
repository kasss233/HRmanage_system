from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

def group_required(*groups):
    """
    Decorator to check if the user is in one of the given groups.
    :param groups: One or more group names.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.groups.filter(name__in=groups).exists():
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
