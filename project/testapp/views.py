from django.shortcuts import render
from testapp.models import employee
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.urls import reverse_lazy
def home(request):
    return render(request, "home.html")
class show_list(ListView):
    model = employee
    template_name="list.html"
    extra_context={"title":"列表"}
    context_object_name = "employees"  # 修改上下文变量名称
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")  # 搜索关键词
        search_by = self.request.GET.get("search_by", "name")  # 搜索字段，默认按 name 搜索
        if query:
            if search_by == "name":
                queryset = queryset.filter(name__icontains=query)
            elif search_by == "email":
                queryset = queryset.filter(email__icontains=query)
            elif search_by == "phone":
                queryset = queryset.filter(phone__icontains=query)
        # 排序功能
        order_by = self.request.GET.get("order_by", "id")  # 默认按 ID 排序
        order_dir = self.request.GET.get("order_dir", "asc")  # 默认升序
        if order_dir == "desc":
            order_by = f"-{order_by}"
        queryset = queryset.order_by(order_by)

        return queryset
class EmployeeUpdateView(UpdateView):
    model = employee
    fields = ['name', 'email', 'phone']  # 可编辑的字段
    template_name = 'edit_employee.html'
    success_url = reverse_lazy('list')  # 编辑成功后重定向
class EmployeeCreateView(CreateView):
    model = employee
    fields = ['id', 'name', 'email', 'phone']  # 定义表单字段
    template_name = 'add_employee.html'
    success_url = reverse_lazy('list')  # 添加成功后跳转到列表页面
    
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from testapp.models import employee

class EmployeeDeleteView(DeleteView):
    model = employee
    template_name = 'confirm_delete.html'  # 删除确认页面模板
    success_url = reverse_lazy('list')  # 删除成功后跳转到列表页面

from django.http import HttpResponse
import csv
def export_employees_csv(request):
    # 定义 HTTP 响应类型为 CSV 文件
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'

    # 创建 CSV 写入器
    writer = csv.writer(response)
    # 写入表头
    writer.writerow(['ID', 'Name', 'Email', 'Phone'])

    # 查询所有员工数据并写入 CSV
    employees = employee.objects.all()
    for emp in employees:
        writer.writerow([emp.id, emp.name, emp.email, emp.phone])

    return response