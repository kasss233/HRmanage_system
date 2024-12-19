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
from django.core.paginator import Paginator
def list_view(request):
    form = AttendanceFilterForm(request.GET, user=request.user)
    attendance_records = Attendance.objects.all()

    if form.is_valid():
        # 获取筛选字段
        id=form.cleaned_data.get('id')
        name = form.cleaned_data.get('name')
        employee = form.cleaned_data.get('employee')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        department = form.cleaned_data.get('department')
        # 根据条件进行过滤
        if id:
            attendance_records = attendance_records.filter(employee__id__icontains=id)
        if name:
            attendance_records = attendance_records.filter(employee__name__icontains=name)
        if employee:
            attendance_records = attendance_records.filter(employee=employee)
        if start_date:
            attendance_records = attendance_records.filter(date__gte=start_date)
        if end_date:
            attendance_records = attendance_records.filter(date__lte=end_date)
        if department:
            attendance_records = attendance_records.filter(employee__department=department)
        
    # 分页逻辑
    attendance_records = attendance_records.order_by('-date')  # 排序可以调整为你需要的字段
    paginator = Paginator(attendance_records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 渲染模板并传递数据
    return render(request, 'attendance_list.html', {
        'form': form,
        'attendance_records': page_obj,
        'query_params': request.GET.urlencode(),  # 保持查询参数以便分页使用
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
    is_out_of_range = False  # 添加一个变量来标识是否在时间范围内

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
            sign_in_start = time(0, 0)  # 1:00
            sign_in_end = time(23, 59)  # 23:30

            if sign_in_start <= current_time.time() <= sign_in_end:
                # 创建考勤记录或更新考勤记录
                attendance, created = Attendance.objects.get_or_create(employee=employee_instance, is_sign_in=False)
                attendance.date = localtime(now()).date()
                attendance.sign_in = localtime(now())
                attendance.is_sign_in = True
                attendance.save()
            else:
                # 签到时间不在有效范围内，设置标识为 True
                is_out_of_range = True
        elif not is_signed_out:  # 如果已签到但未签退
            # 判断当前时间是否在签退时间段内
            sign_out_start = time(0, 0)  # 9:00
            sign_out_end = time(23, 59)  # 18:00

            if sign_out_start <= current_time.time() <= sign_out_end:
                # 记录签退时间
                today_attendance.sign_out = localtime(now())
                today_attendance.is_sign_out = True
                today_attendance.save()
            else:
                # 签退时间不在有效范围内，设置标识为 True
                is_out_of_range = True

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
        'is_out_of_range': is_out_of_range,  # 添加提示信息标识
    }

    return render(request, 'attendance_sign.html', context)


