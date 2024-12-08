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
urlpatterns = [
    path("admin/", admin.site.urls),
    path('',testapp.views.show_list.as_view(), name='list'),
    #path('list/',testapp.views.show_list.as_view(), name='list'),
    path('employees/edit/<int:pk>/', testapp.views.EmployeeUpdateView.as_view(), name='employee_edit'),  # 编辑视图
    path('employees/add/', testapp.views.EmployeeCreateView.as_view(), name='employee_add'),
    path('delete/<int:pk>/', testapp.views.EmployeeDeleteView.as_view(), name='employee_delete'),  # 删除员工
    path('export/', testapp.views.export_employees_csv, name='employee_export'),  # 导出功能路由
]
