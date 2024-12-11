from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from employee.forms import EmployeeForm
from django.urls import reverse_lazy
from .models import employee

from django.shortcuts import render
from django.views.generic import ListView
from datetime import date
from .models import employee
from .forms import EmployeeFilterForm

class list_view(ListView):
    model = employee
    template_name = 'employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10  # 每页显示10条记录

    def get_queryset(self):
        queryset = employee.objects.all()

        # 获取查询参数
        name = self.request.GET.get('name', '')
        sex = self.request.GET.get('sex', '')
        min_age = self.request.GET.get('min_age', '')
        max_age = self.request.GET.get('max_age', '')

        # 按照查询条件过滤
        if name:
            queryset = queryset.filter(name__icontains=name)
        if sex:
            queryset = queryset.filter(sex=sex)

        today = date.today()

        # 计算最小年龄的过滤
        if min_age:
            try:
                min_age = int(min_age)
                min_birthday = today.replace(year=today.year - min_age)
                queryset = queryset.filter(birthday__lte=min_birthday)
            except ValueError:
                pass  # 如果转换失败，忽略该条件

        # 计算最大年龄的过滤
        if max_age:
            try:
                max_age = int(max_age)
                max_birthday = today.replace(year=today.year - max_age)
                queryset = queryset.filter(birthday__gte=max_birthday)
            except ValueError:
                pass  # 如果转换失败，忽略该条件

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 添加筛选表单数据
        context['form'] = EmployeeFilterForm(self.request.GET)
        return context


class create_view(CreateView):
    model = employee
    template_name = 'employee_create.html'  # 模板文件路径
    form_class = EmployeeForm  # 使用自定义的表单类
    success_url = reverse_lazy('employee_list')  # 保存成功后重定向到列表视图



class delete_view(DeleteView):
    model = employee
    template_name = 'employee_delete.html'  # 确认删除页面模板
    success_url = reverse_lazy('employee_list')  # 删除成功后重定向到员工列表视图



class update_view(UpdateView):
    model = employee
    template_name = 'employee_update.html'  # 模板文件路径
    form_class = EmployeeForm  # 使用自定义的表单类
    success_url = reverse_lazy('employee_list')  # 更新成功后重定向到列表视图




