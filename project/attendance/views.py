from django.shortcuts import render
from .forms import AttendanceFilterForm
from .models import Attendance
from django.utils.decorators import method_decorator
from .decorators import group_required
from django.contrib.auth.decorators import login_required
from employee.models import employee
from django.shortcuts import render, redirect
from django.utils.timezone import localtime
from django.http import HttpResponse
from .models import Attendance
from datetime import time
from django.utils.timezone import localtime, now
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime, now
from .models import Attendance
from employee.models import employee
from datetime import time
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


@login_required
def sign(request):
    user = request.user
    employee_instance = user.employee  # 假设 Employee 模型与 User 之间有一对一关系

    # 获取当前时间
    current_time = localtime(now())
    sign_in_time = None
    sign_out_time = None
    is_signed_in = False
    is_signed_out = False

    # 获取今天的考勤记录
    today_attendance = Attendance.objects.filter(employee=employee_instance, date=current_time.date()).first()

    if today_attendance:
        sign_in_time = today_attendance.sign_in
        sign_out_time = today_attendance.sign_out
        is_signed_in = today_attendance.is_sign_in
        is_signed_out = today_attendance.is_sign_out

    # 处理签到或签退请求
    if request.method == 'POST':
        if not is_signed_in:  # 如果没有签到
            # 判断当前时间是否在签到时间段内
            sign_in_start = time(1, 0)  # 1:00
            sign_in_end = time(23, 30)  # 23:30

            if sign_in_start <= current_time.time() <= sign_in_end:
                # 创建考勤记录或更新考勤记录
                attendance, created = Attendance.objects.get_or_create(employee=employee_instance, is_sign_in=False)
                attendance.date = localtime(now()).date()
                attendance.sign_in = localtime(now())
                attendance.is_sign_in = True
                attendance.save()
            else:
                # 签到时间不在有效范围内，不执行任何操作
                pass
        elif not is_signed_out:  # 如果已签到但未签退
            # 记录签退时间
            today_attendance.sign_out = localtime(now())
            today_attendance.is_sign_out = True
            today_attendance.save()

    # 重新获取今天的考勤记录，以便显示最新的状态
    today_attendance = Attendance.objects.filter(employee=employee_instance, date=current_time.date()).first()

    if today_attendance:
        sign_in_time = today_attendance.sign_in
        sign_out_time = today_attendance.sign_out
        is_signed_in = today_attendance.is_sign_in
        is_signed_out = today_attendance.is_sign_out

    context = {
        'current_time': current_time,
        'employee': employee_instance,
        'sign_in_time': sign_in_time,
        'sign_out_time': sign_out_time,
        'is_signed_in': is_signed_in,
        'is_signed_out': is_signed_out,
    }

    return render(request, 'attendance_sign.html', context)

