from django.contrib import admin
from django.urls import path
from employee import views
import group.views
import attendance.views
import accounts.views

urlpatterns = [
    path("admin/", admin.site.urls),
    # 员工相关路径
    path("employee/", views.list_view.as_view(), name="employee_list"),  # 使用类视图时要加 .as_view()
    path("employee/create/", views.create_view.as_view(), name="employee_create"),
    path("employee/delete/<int:pk>/", views.delete_view.as_view(), name="employee_delete"),
    path("employee/update/<int:pk>/", views.update_view.as_view(), name="employee_update"),
    
    # 考勤相关路径
    path("attendance/", attendance.views.list_view, name="attendance_list"),  # 假设是函数视图
    path("sign", attendance.views.sign, name="sign"),  # 假设是签到的函数视图
    
    # 账户相关路径
    path("", accounts.views.login_view, name="login"),
    path("login/", accounts.views.login_view, name="login"),
    path("register/", accounts.views.register_view, name="register"),
    path("logout/", accounts.views.logout_view, name="logout"),

    # 创建小组的路径
    path('group/create_groups/', group.views.create_groups_view, name='create_groups'),
]
