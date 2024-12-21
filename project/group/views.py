from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from employee.decorators import group_required
from employee.models import group
from django.contrib import messages
from employee.forms import CreateGroupsForm,EmployeeFilterForm
from django.shortcuts import redirect
from .service import create_groups_for_department


def create_groups_view(request):
    # 判断用户是否为总经理或部门经理
    user = request.user
    is_manager = user.groups.filter(name='manager').exists()
    is_department_manager = user.groups.filter(name='department_manager').exists()

    if is_department_manager:
        current_department = user.employee.department  # 假设用户模型中有 department 字段
    else:
        current_department = None  # 总经理可以管理所有部门，所以设置为 None
    
    if request.method == 'POST':
        department_name = request.POST.get('department')
        
        if not department_name:
            messages.error(request, "请选择一个部门")
            return redirect('create_groups')  # 重定向回创建页面
        
        # 调用函数创建小组
        result = create_groups_for_department(department_name)
        messages.success(request, result)  # 显示成功/错误消息
        return redirect('create_groups')  # 重定向回创建页面

    # 如果是 GET 请求，显示创建小组的页面
    form = EmployeeFilterForm(user=request.user)
    
    # 返回页面时传递是否是总经理、部门经理以及当前部门的状态
    return render(request, 'create_groups.html', {
        'form': form,
        'is_manager': is_manager,  # 是否是总经理
        'is_department_manager': is_department_manager,  # 是否是部门经理
        'current_department': current_department  # 当前部门
    })

# Create your views here.
@login_required()  # 只保留这个
@group_required('department_manager', 'general_manager')
def create_groups(request):
    user = request.user

    # 检查是否为总经理或部门经理
    is_manager = user.groups.filter(name='manager').exists()
    is_department_manager = user.groups.filter(name='department_manager').exists()

    # 如果不是总经理或部门经理，返回一个权限不足的提示
    if not is_manager and not is_department_manager:
        return render(request, 'error.html', {'message': "您没有权限访问此页面。只有总经理和部门经理可以创建小组。"})

    # 当前部门默认从用户信息中获取（假设用户模型有部门字段）
    current_department = user.employee.department if not is_manager else None

    # 处理表单提交
    form = CreateGroupsForm(request.POST or None, user=user, current_department=current_department)

    # 如果表单提交并且有效
    if request.method == "POST" and form.is_valid():
        department_name = form.cleaned_data['department']
        result = create_groups_for_department(department_name)
        
        # 返回页面时传递创建结果、当前部门信息和是否为经理的状态
        return render(request, 'create_groups.html', {
            'form': form, 
            'result': result, 
            'current_department': department_name, 
            'is_manager': is_manager,
            'is_department_manager': is_department_manager
        })
