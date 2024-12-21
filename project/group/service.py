from django.http import HttpResponse
from django.shortcuts import render
from employee.forms import EmployeeFilterForm
from django.db import transaction
from employee.models import employee,group

def create_groups_for_department(department_name):
    # 获取指定部门的所有员工，排除已经有小组的员工
    employees = employee.objects.filter(department=department_name, group__isnull=True)

    if not employees.exists():
        return "没有员工可以分配到小组"

    # 每个小组最多 4 人
    group_size = 4
    group_count = (employees.count() // group_size) + (1 if employees.count() % group_size != 0 else 0)

    with transaction.atomic():
        # 创建小组并分配员工
        for i in range(group_count):
            group_name = f"{department_name} - 小组{i+1}"
            group = group.objects.create(department=department_name, name=group_name)

            # 为每个小组分配成员
            group_members = employees[i*group_size:(i+1)*group_size]
            group.employees.set(group_members)

            # 更新员工的 group 字段
            for employee in group_members:
                employee.group = group
                employee.save()

    return f"小组创建完成：{group_count}个小组"
def assign_group_leader(request):
    if request.method == 'POST':
        form = EmployeeFilterForm(request.POST, user=request.user)
        if form.is_valid():
            group = form.cleaned_data['group']
            leader = form.cleaned_data['leader']
            
            if group and leader:
                # 如果当前用户是部门经理，更新小组的组长
                if request.user.groups.filter(name='department_manager').exists():
                    group.leader = leader
                    group.save()
                    return HttpResponse("组长任命成功！")
                else:
                    return HttpResponse("您没有权限任命组长。")
            else:
                return HttpResponse("请选择小组和组长。")
    else:
        form = EmployeeFilterForm(user=request.user)

    return render(request, 'assign_group_leader.html', {'form': form})

def assign_group_member(request):
    if request.method == 'POST':
        form = EmployeeFilterForm(request.POST, user=request.user)
        if form.is_valid():
            group = form.cleaned_data['group']
            employee_member = form.cleaned_data['employee_member']
            
            if group and employee_member:
                # 根据选择的身份（组长、部门经理或总经理）执行相关操作
                if request.user.groups.filter(name='department_manager').exists():
                    # 部门经理操作，处理部门内小组成员
                    print(f"部门经理：将成员 {employee_member.name} 添加到小组 {group.name}")
                    return HttpResponse("操作成功！")
                elif request.user.groups.filter(name='team_leader').exists():
                    # 组长操作，处理组长所属小组的成员
                    print(f"组长：将成员 {employee_member.name} 添加到小组 {group.name}")
                    return HttpResponse("操作成功！")
                elif request.user.groups.filter(name='super_manager').exists():
                    # 总经理操作，处理所有小组成员
                    print(f"总经理：将成员 {employee_member.name} 添加到小组 {group.name}")
                    return HttpResponse("操作成功！")
                else:
                    return HttpResponse("您没有权限进行此操作")
            else:
                return HttpResponse("请选择小组和成员")
    else:
        form = EmployeeFilterForm(user=request.user)

    return render(request, 'assign_group_member.html', {'form': form})

