from django.shortcuts import render, get_object_or_404
from .models import Salary, SalaryStandard

# 查询员工工资
def salary_detail(request, employee_id):
    salary = get_object_or_404(Salary, id=employee_id)
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
