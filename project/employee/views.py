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
from django.views.generic import ListView
from datetime import date
from .models import employee
from .forms import EmployeeFilterForm
from django.db.models import Q
from .decorators import group_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password

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
        birthday = self.request.GET.get('birthday', '').strip()
        # 按照查询条件过滤
        if name:
            queryset = queryset.filter(name__icontains=name)
        if sex:
            queryset = queryset.filter(sex=sex)
        if birthday:
            queryset = queryset.filter(birthday=birthday)
        today = date.today()
        

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


@method_decorator(group_required('manager'), name='dispatch')
class create_view(CreateView):
    model = employee
    template_name = 'employee_create.html'  # 模板文件路径
    form_class = EmployeeForm  # 使用自定义的表单类
    success_url = reverse_lazy('employee_list')  # 保存成功后重定向到列表视图
    def form_valid(self, form):
        # 首先保存员工对象
        employee = form.save()

        # 创建与员工相关联的用户
        username = str(employee.id)  # 使用员工的ID作为用户名
        password = str(employee.id)  # 使用员工的ID作为密码
        
        # 创建用户并设置密码
        user = User.objects.create(
            username=username,
            password=make_password(password)  # 对密码进行加密存储
        )
        
        # 将用户添加到 'employee' 组
        if employee.position=='普通员工' or employee.position=='试用员工':
            employee_group = Group.objects.get(name='employee')
            user.groups.add(employee_group)
        elif employee.position=='部门经理'or employee.position=='总经理':
            employee_group = Group.objects.get(name='manager')
            user.groups.add(employee_group)
        
        # 将用户与员工关联
        employee.user = user
        employee.save()

        return super().form_valid(form)

@method_decorator(group_required('manager'), name='dispatch')
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
@method_decorator(group_required('manager'), name='dispatch')
class update_view(UpdateView):
    model = employee
    template_name = 'employee_update.html'  # 模板文件路径
    form_class = EmployeeForm  # 使用自定义的表单类
    def form_valid(self, form):
        employee = form.save()
        if employee.position=='普通员工' or employee.position=='试用员工':
            employee_group = Group.objects.get(name='employee')
            employee.user.groups.add(employee_group)
        elif employee.position=='部门经理':
            employee_group = Group.objects.get(name='department_manager')
            employee.user.groups.add(employee_group)
        elif employee.position=='总经理':
            employee_group = Group.objects.get(name='general_manager')
            employee.user.groups.add(employee_group)
        elif employee.position=='员工组长':
            employee_group = Group.objects.get(name='group_leader')
            employee.user.groups.add(employee_group)
        employee.save()
        return super().form_valid(form)
    success_url = reverse_lazy('employee_list')  # 更新成功后重定向到列表视图




