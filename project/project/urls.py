"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
import testapp.views
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
    path("login/",accounts.views.login_view,name="login"),
    path("register/",accounts.views.register_view,name="register"),
    path("logout/",accounts.views.logout_view,name="logout"),
    path("sign",attendance.views.sign,name="sign"),
    path('employee/salary/<int:employee_id>/', salary.views.salary_detail, name='salary_detail'),
    path('standards/', salary.views.standard_detail, name='standard_detail'),
    path('group/create/', group.views.CreateGroupView.as_view(), name='create_group'),
    path('group/<int:pk>/add_member/', group.views.AddMemberToGroupView.as_view(), name='add_member_to_group'),
    path('group/<int:pk>/assign_leader/', group.views.AssignGroupLeaderView.as_view(), name='assign_group_leader'),
    path('attendance/update/<int:pk>/', attendance.views.AttendanceUpdateView.as_view(), name='attendance_update'),
    path('group-management/', group.views.GroupManagementView.as_view(), name='group_management'),
     path('group/<int:group_id>/revoke_leader/', group.views.RevokeGroupLeaderView.as_view(), name='revoke_leader'),  # 添加撤销组长的 URL 路由
    path('group/<int:pk>/delete/', group.views.DeleteGroupView.as_view(), name='delete_group'),
]
