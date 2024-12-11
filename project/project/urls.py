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
import attendance.views
import accounts.views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("employee/",employee.views.list_view.as_view(),name="employee_list"),
    path("employee/create/",employee.views.create_view.as_view(),name="employee_create"),
    path("employee/delete/<int:pk>/",employee.views.delete_view.as_view(),name="employee_delete"),
    path("employee/update/<int:pk>/",employee.views.update_view.as_view(),name="employee_update"),
    path("attendance/",attendance.views.list_view,name="attendance_list"),
    path("",employee.views.list_view.as_view(),name="employee_list"),
    path("login/",accounts.views.login_view,name="login"),
    path("register/",accounts.views.register_view,name="register"),
    path("logout/",accounts.views.logout_view,name="logout"),
]
