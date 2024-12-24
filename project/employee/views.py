import decimal
from django.contrib import messages
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
from salary.models import Salary, SalaryStandard
from .forms import EmployeeFilterForm
from django.db.models import Q
from .decorators import group_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
import csv
from django.http import HttpResponse,HttpResponseForbidden
from urllib.parse import urlencode
@method_decorator(group_required('department_manager', 'general_manager', 'group_leader'), name='dispatch')
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
        details = self.request.GET.get('details', '').strip()
        group=self.request.GET.get('group','').strip()
        
        if user.groups.filter(name='department_manager').exists():
            department = user.employee.department
        elif user.groups.filter(name='group_leader').exists():
            group = user.employee.group
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
        if details:
            queryset = queryset.filter(details__icontains=details)
        if group:
            queryset = queryset.filter(group__name=group)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EmployeeFilterForm(self.request.GET, user=self.request.user)
        query_params = self.request.GET.dict()
        query_params.pop('page', None)  # 删除分页参数，但保留其他筛选参数
        # 传递 query_params 供模板分页器使用
        context['query_params'] = urlencode(query_params)
        context['is_group_leader'] = self.request.user.groups.filter(name="group_leader").exists()
        return context

    def get(self, request, *args, **kwargs):
        # 如果用户请求导出数据
        if 'export' in request.GET:
            return self.export_data()

        # 如果用户请求发放工资
        elif 'pay_salaries' in request.GET:
            return self.pay_salaries()

        # 默认返回父类的 GET 方法
        return super().get(request, *args, **kwargs)

    def export_data(self):
        queryset = self.get_queryset()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="employees.csv"'
        response.charset = 'GBK'
        # 写入 CSV 文件内容
        writer = csv.writer(response)
        writer.writerow(['ID', '姓名', '性别', '生日', '邮箱', '电话', '地址', '部门', '职位','技能'])  # 表头
        for emp in queryset:
            writer.writerow([
                emp.id,
                emp.name,
                emp.sex,
                emp.birthday,
                emp.email,
                emp.phone,
                emp.address,
                emp.department,
                emp.position,
                emp.details
            ])
        return response

    def pay_salaries(self):
        user = self.request.user
        print("Hello")
        # 验证用户是否有权限
        if not user.groups.filter(name__in=['department_manager', 'general_manager', 'group_leader']).exists():
            return HttpResponseForbidden("您没有权限执行此操作！")

        # 获取所有符合条件的员工
        employees = self.get_queryset()
        print(employees)
        # 批量更新工资状态
        for emp in employees:
            salary, created = Salary.objects.get_or_create(id=emp.id)
            print(salary)
            salary.payment_status = '已发'
            salary.save()

        # 重定向回员工列表页面，并显示成功信息
        messages.success(self.request, f"成功发放 {employees.count()} 位员工的工资！")
        return redirect('employee_list')
    
@method_decorator(group_required('department_manager', 'general_manager'), name='dispatch')
class create_view(CreateView):
    model = employee
    template_name = 'employee_create.html'  # 模板文件路径
    form_class = EmployeeForm  # 使用自定义的表单类
    success_url = reverse_lazy('employee_list')  # 保存成功后重定向到列表视图
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        # 获取表单的初始参数
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # 将当前用户传递给表单
        return kwargs
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
        print(f"用户 {username} 创建成功")
        print(f"员工 {employee.name} 的职位是 {employee.position}")
        # 将用户添加到 'employee' 组
        level = 4
        if employee.position=='普通员工' or employee.position=='试用员工':
            employee_group = Group.objects.get(name='employee')
            employee.user.groups.add(employee_group)
            if employee.position == '普通员工':
                level = 4
            else:
                level = 5
        elif employee.position=='部门经理':
            employee_group = Group.objects.get(name='department_manager')
            employee.user.groups.add(employee_group)
            level = 2
        elif employee.position=='总经理':
            employee_group = Group.objects.get(name='general_manager')
            employee.user.groups.add(employee_group)
            level = 1
        elif employee.position=='员工组长':
            employee_group = Group.objects.get(name='group_leader')
            employee.user.groups.add(employee_group)
            level = 4
        # 创建 Salary 记录并保存

        Salary.objects.create(
            id=employee.id,
            level=level,
            bonus=0.00,  # 默认奖金为 0
            total_salary=None  # 总工资将在后端计算
        )

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
    
@method_decorator(group_required('department_manager', 'general_manager','group_leader'), name='dispatch')
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
        level=4
        if employee.position=='普通员工' or employee.position=='试用员工':
            employee_group = Group.objects.get(name='employee')
            employee.user.groups.add(employee_group)
            employee.user.groups.remove(Group.objects.get(name='group_leader'))
            employee.user.groups.remove(Group.objects.get(name='department_manager'))
            employee.user.groups.remove(Group.objects.get(name='general_manager'))
            if employee.position == '普通员工':
                level = 4
            else:
                level = 5
        elif employee.position=='部门经理':
            employee_group = Group.objects.get(name='department_manager')
            employee.user.groups.add(employee_group)
            employee.user.groups.remove(Group.objects.get(name='group_leader'))
            employee.user.groups.remove(Group.objects.get(name='employee'))
            employee.user.groups.remove(Group.objects.get(name='general_manager'))
            level = 2
        elif employee.position=='总经理':
            employee_group = Group.objects.get(name='general_manager')
            employee.user.groups.add(employee_group)
            employee.user.groups.remove(Group.objects.get(name='group_leader'))
            employee.user.groups.remove(Group.objects.get(name='department_manager'))
            employee.user.groups.remove(Group.objects.get(name='employee'))
            level = 1
        elif employee.position=='员工组长':
            employee_group = Group.objects.get(name='group_leader')
            employee.user.groups.add(employee_group)
            employee.user.groups.remove(Group.objects.get(name='department_manager'))
            employee.user.groups.remove(Group.objects.get(name='general_manager'))
            employee.user.groups.remove(Group.objects.get(name='employee'))
            level = 3
        employee.save()
        try:
            salary = Salary.objects.get(id=employee.id)
            salary.level = level
            salary.save()
        except Salary.DoesNotExist:
            Salary.objects.create(
                id=employee.id,
                level=level,
                bonus=0.00,
                total_salary=None
            )
        return super().form_valid(form)
    success_url = reverse_lazy('employee_list')  # 更新成功后重定向到列表视图


from django.db.models import Q


@method_decorator(group_required('department_manager', 'general_manager', 'employee','group_leader'), name='dispatch')
class frontpage_view(LoginRequiredMixin, DetailView):
    model = employee  # 你的员工模型
    template_name = 'employee_frontpage.html'  # 渲染模板
    context_object_name = 'employee'  # 在模板中使用 'employee' 来访问员工对象

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 获取当前员工
        id = self.request.user.employee.id

        # 获取员工的工资记录
        salary_records = Salary.objects.filter(id=id)

        # 将数据传递到模板
        context['salary_records'] = salary_records
        for salary in salary_records:
            salary.save()
        salary_records = Salary.objects.filter(id=id)
        # 将处理后的 salary_records 传入上下文
        context['salary_records'] = salary_records
        # 检查用户是否为组长、部门经理、总经理
        if self.request.user.groups.filter(Q(name='group_leader') | Q(name='general_manager') |Q(name='department_manager')).exists():
            context['is_group_leader'] = True
        else:
            context['is_group_leader'] = False

        return context
    def get_object(self, queryset=None):
        # 获取当前登录用户对应的员工对象
        return self.request.user.employee  # 通过 request.user 获取当前用户的 Employee 关联对象
from django.shortcuts import render
from django.views.generic import DetailView
from .models import employee
@method_decorator(group_required('department_manager', 'general_manager', 'group_leader'), name='dispatch')
class EmployeeDetailView(DetailView):
    model = employee
    template_name = 'employee_detail.html'  # 创建新的模板
    context_object_name = 'employee'  # 模板中使用 'employee' 来访问员工对象

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from salary.models import Salary
from employee.models import employee
from django.http import Http404
@login_required
def update_bonus(request, employee_id):
    try:
        # 获取员工对象
        em = employee.objects.get(id=employee_id)
    except employee.DoesNotExist:
        raise Http404("Employee not found")

    # 获取或创建对应的 Salary 对象
    salary, created = Salary.objects.get_or_create(id=em.id)

    if request.method == 'POST':
        # 获取表单提交的奖金值
        bonus = request.POST.get('bonus')

        if bonus:
            # 更新奖金字段
            salary.bonus = decimal.Decimal(bonus)
            # 调用实例方法保存
            salary.save()  # 自动调用自定义的 save() 方法，计算 total_salary

        return redirect('employee_detail', em.id)  # 更新后重定向到员工详情页

    return redirect('employee_list')  # 如果不是 POST 请求，返回员工列表
