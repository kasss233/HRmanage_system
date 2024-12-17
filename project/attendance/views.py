from django.shortcuts import render
from .forms import AttendanceFilterForm
from .models import Attendance
from django.utils.decorators import method_decorator
from .decorators import group_required
from django.contrib.auth.decorators import login_required
def list_view(request):
    # 获取所有考勤记录
    attendance_records = Attendance.objects.all()

    # 创建并处理筛选表单
    form = AttendanceFilterForm(request.GET)
    
    # 过滤员工列表（如果提供了姓名筛选）
    form.filter_employees()

    if form.is_valid():
        # 根据筛选条件过滤考勤记录
        if form.cleaned_data['employee']:
            attendance_records = attendance_records.filter(employee=form.cleaned_data['employee'])
        if form.cleaned_data['start_date']:
            attendance_records = attendance_records.filter(sign_in__gte=form.cleaned_data['start_date'])
        if form.cleaned_data['end_date']:
            attendance_records = attendance_records.filter(sign_out__lte=form.cleaned_data['end_date'])

    # 分页功能（可选）
    from django.core.paginator import Paginator
    paginator = Paginator(attendance_records, 10)  # 每页显示 10 条记录
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 将表单和考勤记录传递到模板
    return render(request, 'attendance_list.html', {
        'form': form,
        'attendance_records': page_obj,
        'query_params': request.GET.urlencode(),  # 保留查询参数用于分页
    })
from django.shortcuts import render, redirect
from django.utils.timezone import localtime
from django.http import HttpResponse
from .models import Attendance
from datetime import time
from django.utils.timezone import localtime, now
@login_required
def sign_in(request):
    employee = request.user  # 当前登录的用户
    current_time = localtime(now()).time()  # 获取当前时间并转换为本地时间
    # 设定签到时间的允许范围
    sign_in_start = time(8, 0)  # 8:00
    sign_in_end = time(8, 30)  # 8:30

    if sign_in_start <= current_time <= sign_in_end:  # 当前时间在签到时间段内
        # 记录签到时间
        attendance, created = Attendance.objects.get_or_create(employee=employee, is_sign_in=False)

        attendance.sign_in = localtime(now())  # 记录签到时间
        attendance.is_sign_in = True  # 标记为已签到
        attendance.save()

        return HttpResponse("签到成功！")
    else:
        # 当前时间不在签到范围内
        attendance, created = Attendance.objects.get_or_create(employee=employee, is_sign_in=False)

        attendance.is_sign_in = False  # 标记为未签到
        attendance.save()

        return HttpResponse("签到失败，签到时间应在8:00到8:30之间。")
@login_required
def sign_out(request):
    employee = request.user  # 当前登录的用户
    attendance = Attendance.objects.filter(employee=employee, is_sign_in=True).last()

    if attendance:  # 如果该员工已经签到
        attendance.sign_out = localtime(now())  # 记录签退时间
        attendance.is_sign_out = True  # 标记为已签退
        attendance.save()

        return HttpResponse("签退成功！")
    else:
        return HttpResponse("您尚未签到，无法签退。")
