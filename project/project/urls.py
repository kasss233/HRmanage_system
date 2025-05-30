from django.contrib import admin
from django.urls import path
import employee.views
import group.views
import attendance.views
import accounts.views
import attendance.views
import salary.views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("employee/",employee.views.list_view.as_view(),name="employee_list"),
    path("frontpage",employee.views.frontpage_view.as_view(),name="employee_frontpage"),
    path("employee/create/",employee.views.create_view.as_view(),name="employee_create"),
    path("employee/delete/<int:pk>/",employee.views.delete_view.as_view(),name="employee_delete"),
    path("employee/update/<int:pk>/",employee.views.update_view.as_view(),name="employee_update"),
    path("attendance/",attendance.views.list_view,name="attendance_list"),
    path("",accounts.views.login_view,name="login"),
    path("register/",accounts.views.register_view,name="register"),
    path("logout/",accounts.views.logout_view,name="logout"),
    path("sign",attendance.views.sign,name="sign"),
    path('employee/salary/<int:employee_id>/', salary.views.salary_detail, name='salary_detail'),
    path('standards/', salary.views.standard_detail, name='standard_detail'),
    path('standard_settings/', salary.views.standard_settings, name='standard_settings'),  # 新建工资标准设置页面
    path('standards/update/<str:standard_no>/', salary.views.update_salary_standard, name='update_salary_standard'),
    path('employee/<int:employee_id>/update_bonus/', employee.views.update_bonus, name='update_bonus'),
    path('standard_settings/<int:standard_id>/', salary.views.standard_settings, name='standard_settings_edit'),  # 编辑工资标准页面
    path('group/create/', group.views.CreateGroupView.as_view(), name='create_group'),
    path('group/<int:pk>/assign_leader/', group.views.AssignGroupLeaderView.as_view(), name='assign_group_leader'),
    path('attendance/update/<int:pk>/', attendance.views.AttendanceUpdateView.as_view(), name='attendance_update'),
    path('group-management/', group.views.GroupManagementView.as_view(), name='group_management'),
    path('group/<int:group_id>/revoke_leader/', group.views.RevokeGroupLeaderView.as_view(), name='revoke_leader'),  # 添加撤销组长的 URL 路由
    path('group/<int:pk>/delete/', group.views.DeleteGroupView.as_view(), name='delete_group'),
    path('employee/<int:pk>/', employee.views.EmployeeDetailView.as_view(), name='employee_detail'),  # 新增详细信息页面
    path('group/<int:pk>/', group.views.GroupDetailView.as_view(), name='group_detail'),
    path("reset_password/", accounts.views.reset_password, name="reset_password"),
]

