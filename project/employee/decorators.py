from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib.auth.decorators import login_required

def group_required(group_name):
    """
    自定义装饰器：检查用户是否属于指定的用户组
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required  # 确保用户已登录
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("您没有权限访问此页面！")
        return wrapper
    return decorator
