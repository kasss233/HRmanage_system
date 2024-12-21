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
        user = self.request.user
        # 获取查询参数，避免传入空字符串
        name = self.request.GET.get('name', '').strip()
        sex = self.request.GET.get('sex', '').strip()
        birthday = self.request.GET.get('birthday', '').strip()
        department = self.request.GET.get('department', '').strip()
        group = self.request.GET.get('group', '').strip()
        if user.groups.filter(name='department_manager').exists():
            department = user.employee.department
        # 按照查询条件过滤
        if name:
            queryset = queryset.filter(name__icontains=name)
        if sex:
            queryset = queryset.filter(sex=sex)
        if birthday:
            queryset = queryset.filter(birthday=birthday)
        if department:
            queryset = queryset.filter(department=department)
        if group:
            queryset = queryset.filter(group__name__icontains=group)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 将当前用户传递给表单
        context['form'] = EmployeeFilterForm(self.request.GET, user=self.request.user)

        # 保持分页状态的查询参数（确保翻页时不丢失筛选条件）
        query_params = self.request.GET.copy()
        query_params['page'] = self.request.GET.get('page', 1)  # 防止分页为空
        context['query_params'] = query_params.urlencode()

        return context

@method_decorator(group_required('department_manager', 'general_manager'), name='dispatch')
class create_view(CreateView):
    model = employee
    template_name = 'employee_create.html'  # 模板文件路径
    form_class = EmployeeForm  # 使用自定义的表单类
    success_url = reverse_lazy('employee_list')  # 保存成功后重定向到列表视图
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EmployeeForm(self.request.GET, user=self.request.user)
        return context
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
        employee.user = user
        employee.save()
        # 将用户添加到 'employee' 组
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
        

        return super().form_valid(form)

@method_decorator(group_required('department_manager', 'general_manager'), name='dispatch')
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
    
@method_decorator(group_required('department_manager', 'general_manager'), name='dispatch')
class update_view(UpdateView):
    model = employee
    template_name = 'employee_update.html'  # 模板文件路径
    form_class = EmployeeForm  # 使用自定义的表单类
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        # 获取表单的初始参数
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # 将当前用户传递给表单
        return kwargs
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



