from django import forms
from .models import Attendance
from employee.models import employee
from django.forms.widgets import TextInput
class AttendanceFilterForm(forms.Form):
    # 添加姓名搜索框
    DEPARTMENT_CHOICES = [
        ('技术部', '技术部'),
        ('市场部', '市场部'),
        ('人事部', '人事部'),
        ('财务部', '财务部'),
        ('行政部', '行政部'),
        ('研发部', '研发部'),
        ('销售部', '销售部'),
        ('客服部', '客服部'),
        ('运营部', '运营部'),
        ('采购部', '采购部'),
        ('售后部', '售后部'),
        ('公关部', '公关部'),
        ('战略部', '战略部'),
        ('人力资源部', '人力资源部'),
        ('法务部', '法务部'),
    ]
    name = forms.CharField(
        required=False,
        label='员工姓名',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': '请输入姓名'})
    )
    # 添加员工ID搜索框
    id = forms.IntegerField(
        required=False,
        label='员工ID',
        widget=forms.TextInput(attrs={'placeholder': '请输入员工ID'})
    )
    employee = forms.ModelChoiceField(
        queryset=employee.objects.all(),
        required=False,
        label='员工',
        empty_label="所有员工"
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='开始日期'
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='结束日期'
    )
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select,label='部门',required=False)
    # 提供筛选的默认值
    def __init__(self, *args, **kwargs):
        user=kwargs.pop('user',None)
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = employee.objects.all()
        if user and user.groups.filter(name='department_manager').exists():
            employee_obj = employee.objects.get(user=user)
            current_department = user.employee.department  # 获取当前部门
            # 将 department 字段设置为只读，并默认选中当前部门
            self.fields['department'].initial = current_department
            # 限制 department 字段的选择项为当前部门
            self.fields['department'].choices = [(current_department, current_department)]
            # 禁用部门选择字段
            self.fields['department'].disabled = True  # 禁用字段，不可编辑
            # 使用 TextInput 显示部门名称，并使其不可编辑
            self.fields['department'].widget = TextInput(attrs={'value': current_department, 'readonly': 'readonly'})

    def filter_employees(self):
        # 获取员工姓名和ID搜索字段
        if self.is_valid():
            name = self.cleaned_data.get('name')
            employee_id = self.cleaned_data.get('id')

            # 如果输入了姓名，过滤员工列表
            if name:
                self.fields['employee'].queryset = employee.objects.filter(name__icontains=name)

            # 如果输入了员工ID，过滤员工列表
            if employee_id:
                self.fields['employee'].queryset = self.fields['employee'].queryset.filter(id=employee_id)
