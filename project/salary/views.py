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
def standard_detail(request):
    standards = SalaryStandard.objects.all()
    context = {
        'standards': standards
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
