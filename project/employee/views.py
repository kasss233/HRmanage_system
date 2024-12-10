from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import employee

class list_view(ListView):
    model = employee
    template_name = 'employee_list.html'  # 模板文件路径
    context_object_name = 'employees'  # 模板中使用的上下文变量名
    paginate_by = 10  # 每页显示 10 条记录
    def get_queryset(self):
        """
        重写 get_queryset 方法，添加过滤逻辑。
        根据请求中的筛选条件返回筛选后的员工数据。
        """
        queryset = employee.objects.all()  # 默认查询所有员工

        # 获取请求中的查询参数
        name = self.request.GET.get('name', '')
        sex = self.request.GET.get('sex', '')
        min_age = self.request.GET.get('min_age', '')
        max_age = self.request.GET.get('max_age', '')

        # 根据表单数据进行过滤
        if name:
            queryset = queryset.filter(name__icontains=name)  # 根据姓名进行模糊匹配
        if sex:
            queryset = queryset.filter(sex=sex)
        if min_age:
            # 假设根据生日来计算最小年龄
            queryset = queryset.filter(birthday__lte='1900-01-01')  # 根据实际需求调整
        if max_age:
            queryset = queryset.filter(birthday__gte='1900-01-01')  # 根据实际需求调整

        return queryset

    def get_context_data(self, **kwargs):
        """
        重写 get_context_data 方法，传递表单数据和员工列表到模板
        """
        context = super().get_context_data(**kwargs)
        # 在上下文中添加表单数据以便模板渲染
        context['form'] = EmployeeFilterForm(self.request.GET)  # 表单数据
        return context


class create_view(CreateView):
    model = employee
    template_name = 'employee_create.html'  # 模板文件路径
    fields = ['id', 'name', 'sex', 'birthday', 'email', 'phone', 'address']
    success_url = reverse_lazy('employee_list')  # 保存成功后重定向到列表视图



class delete_view(DeleteView):
    model = employee
    template_name = 'employee_delete.html'  # 模板文件路径
    success_url = reverse_lazy('employee_list')  # 删除成功后重定向到列表视图



class update_view(UpdateView):
    model = employee
    template_name = 'employee_update.html'  # 模板文件路径
    fields = ['id', 'name', 'sex', 'birthday', 'email', 'phone', 'address']
    success_url = reverse_lazy('employee_list')  # 更新成功后重定向到列表视图




from datetime import date
from django.shortcuts import render
from .models import employee
from .forms import EmployeeFilterForm

def employee_list_view(request):
    # 获取筛选表单
    form = EmployeeFilterForm(request.GET)
    
    # 初始化查询集
    employees = employee.objects.all()

    # 如果表单有效且包含筛选条件
    if form.is_valid():
        name = form.cleaned_data.get('name')
        sex = form.cleaned_data.get('sex')
        min_age = form.cleaned_data.get('min_age')
        max_age = form.cleaned_data.get('max_age')
        
        # 逐个检查条件并过滤员工
        if name:
            employees = employees.filter(name__icontains=name)
        if sex:
            employees = employees.filter(sex=sex)
        
        # 计算当前日期和最小/最大年龄的生日范围
        today = date.today()
        
        if min_age:
            min_birthday = today.replace(year=today.year - min_age)
            employees = employees.filter(birthday__lte=min_birthday)
        
        if max_age:
            max_birthday = today.replace(year=today.year - max_age)
            employees = employees.filter(birthday__gte=max_birthday)

    return render(request, 'employee_list.html', {
        'form': form,
        'employees': employees
    })
