from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib.auth.decorators import login_required

def group_required(*group_names):
    """
    Requires user membership in at least one of the given groups.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.groups.filter(name__in=group_names).exists():
                # If the user is not in any of the specified groups
                return HttpResponseForbidden("您没有权限访问此页面！")  # Adjust as necessary for your app
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator