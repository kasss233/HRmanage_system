from django.shortcuts import render, get_object_or_404, redirect
from .models import Salary, SalaryStandard
from django.http import HttpResponse
# 查询员工工资
def salary_detail(request, employee_id):
    salary = get_object_or_404(Salary, id=employee_id)
    salary.save()
    try:
        standard = SalaryStandard.objects.get(id=salary.level)
        basic_salary = standard.basic_salary
    except SalaryStandard.DoesNotExist:
        basic_salary = 0  # 默认基本工资为 0

    total_salary = basic_salary + (salary.bonus or 0)
    salary.total_salary = total_salary
    salary.save()  # 更新 total_salary

    context = {
        'salary': salary,
        'basic_salary': basic_salary,
        'total_salary': total_salary,
    }
    return render(request, 'salary_detail.html', context)


# 查询工资标准
from django.db.models import Q
def standard_detail(request):
    standards = SalaryStandard.objects.all()
    # 检查用户是否属于 "general_manager" 组
    is_general_manager = request.user.groups.filter( Q(name='general_manager')).exists()

    context = {
        'standards': standards,
        'is_general_manager': is_general_manager,  # 将权限信息传递给模板
    }
    return render(request, 'standard_detail.html', context)

# 设置工资标准
def standard_settings(request, standard_id=None):
    if standard_id:
        # 编辑已有的工资标准
        standard = get_object_or_404(SalaryStandard, id=standard_id)
    else:
        # 新建工资标准
        standard = SalaryStandard()

    if request.method == 'POST':
        # 获取提交的表单数据
        standard.standard_no = request.POST.get('standard_no')
        standard.standard_name = request.POST.get('standard_name')
        standard.creator = request.POST.get('creator')
        standard.creation_date = request.POST.get('creation_date')
        standard.basic_salary = request.POST.get('basic_salary')
        standard.standard_status = request.POST.get('standard_status')
        standard.late_deduction = request.POST.get('late_deduction')
        standard.absence_deduction = request.POST.get('absence_deduction')
        standard.full_attendance_bonus = request.POST.get('full_attendance_bonus')

        # 保存工资标准
        standard.save()
        return redirect('standard_detail')  # 保存后重定向到工资标准列表页面

    context = {
        'standard': standard
    }
    return render(request, 'standard_settings.html', context)

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.views import View

def update_salary_standard(request, standard_no):
    # 确认用户是否有权限进行更新
    if not request.user.groups.filter(name__in=['general_manager']).exists():
        return HttpResponseForbidden("您没有权限执行此操作！")

    # 获取对应的工资标准
    salary_standard = get_object_or_404(SalaryStandard, standard_no=standard_no)

    # 检查是否为 POST 请求
    if request.method == 'POST':
        # 从请求中获取新值并更新字段
        salary_standard.standard_name = request.POST.get('standard_name', salary_standard.standard_name)
        salary_standard.basic_salary = request.POST.get('basic_salary', salary_standard.basic_salary)
        salary_standard.late_deduction = request.POST.get('late_deduction', salary_standard.late_deduction)
        salary_standard.absence_deduction = request.POST.get('absence_deduction', salary_standard.absence_deduction)
        salary_standard.full_attendance_bonus = request.POST.get('full_attendance_bonus', salary_standard.full_attendance_bonus)
        salary_standard.standard_status = request.POST.get('standard_status', salary_standard.standard_status)

        # 保存更新后的对象
        salary_standard.save()

        # 返回成功提示并重定向回列表页面
        messages.success(request, f"工资标准编号 {standard_no} 已成功更新！")
        return redirect('standard_detail')  # 替换为工资标准列表页面的 URL 名称

    # 如果不是 POST 请求，则返回错误
    return HttpResponseForbidden("无效的请求方式！")
