from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from employee.forms import EmployeeForm
from .forms import EmployeeDeleteForm
from django.urls import reverse_lazy
from .models import employee
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views.generic import ListView
from datetime import date
from .models import employee
from .forms import EmployeeFilterForm

from django.db.models import Q
from datetime import date
from .forms import EmployeeFilterForm

class list_view(ListView):
    model = employee
    template_name = 'employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10  # 每页显示10条记录
    
    def get_queryset(self):
        queryset = employee.objects.all()

        # 获取查询参数，避免传入空字符串
        name = self.request.GET.get('name', '').strip()
        sex = self.request.GET.get('sex', '').strip()
        min_age = self.request.GET.get('min_age', '').strip()
        max_age = self.request.GET.get('max_age', '').strip()
        birthday = self.request.GET.get('birthday', '').strip()
        # 按照查询条件过滤
        if name:
            queryset = queryset.filter(name__icontains=name)
        if sex:
            queryset = queryset.filter(sex=sex)
        if birthday:
            queryset = queryset.filter(birthday=birthday)
        today = date.today()

        # 计算最小年龄的过滤
        if min_age:
            try:
                min_age = int(min_age)
                min_birthday = today.replace(year=today.year - min_age)
                queryset = queryset.filter(birthday__lte=min_birthday)
            except ValueError:
                # 如果转换失败，可以在这里添加错误信息，或者使用 `pass`
                pass

        # 计算最大年龄的过滤
        if max_age:
            try:
                max_age = int(max_age)
                max_birthday = today.replace(year=today.year - max_age)
                queryset = queryset.filter(birthday__gte=max_birthday)
            except ValueError:
                # 同样可以在这里处理错误
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 添加筛选表单数据，并传递 GET 请求中的参数
        context['form'] = EmployeeFilterForm(self.request.GET)
        
        # 保持分页状态的查询参数（确保翻页时不丢失筛选条件）
        query_params = self.request.GET.copy()
        query_params['page'] = self.request.GET.get('page')
        context['query_params'] = query_params.urlencode()

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
    form_class = EmployeeDeleteForm
    def get_object(self):
        obj = get_object_or_404(employee, pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EmployeeDeleteForm(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        employee = self.get_object()
        employee.delete()
        return redirect(self.success_url)

class update_view(UpdateView):
    model = employee
    template_name = 'employee_update.html'  # 模板文件路径
    form_class = EmployeeForm  # 使用自定义的表单类
    success_url = reverse_lazy('employee_list')  # 更新成功后重定向到列表视图




