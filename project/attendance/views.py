from django.shortcuts import render
from .forms import AttendanceFilterForm
from .models import Attendance

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
