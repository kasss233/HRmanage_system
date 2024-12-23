# decorators.py
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def department_or_general_manager_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not (request.user.is_department_manager or request.user.is_general_manager):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def group_required(*group_names):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not any(request.user.groups.filter(name=group).exists() for group in group_names):
                # 如果用户不在任何一个需要的组内，则拒绝访问
                return redirect('no_permission')  # 这里假设你有权限不足的页面
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

