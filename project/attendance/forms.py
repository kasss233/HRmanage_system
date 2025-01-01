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
    id = forms.IntegerField(
        required=False,
        label='员工ID',
        widget=forms.TextInput(attrs={'placeholder': '请输入员工ID'})
    )
    name = forms.CharField(
        required=False,
        label='员工姓名',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': '请输入姓名'})
    )
    # 添加员工ID搜索框
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
    group=forms.CharField(max_length=100,required=False,label='组名')
    # 提供筛选的默认值
    def __init__(self, *args, **kwargs):
        user=kwargs.pop('user',None)
        super().__init__(*args, **kwargs)
        if user:
            if user.groups.filter(name='department_manager').exists():
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
            elif user.groups.filter(name='general_manager').exists():
                pass
            elif user.groups.filter(name='employee').exists():
                employee_obj = employee.objects.get(user=user)
                self.fields['group'].disabled = True  # 禁用字段，不可编辑
                self.fields['department'].disabled = True
                self.fields['name'].disabled = True
                self.fields['id'].disabled = True
            elif user.groups.filter(name='group_leader').exists():
                employee_obj = employee.objects.get(user=user)
                self.fields['group'].disabled = True  # 禁用字段，不可编辑
                self.fields['group'].initial = employee_obj.group  # 设置默认值为当前用户所属的组
                self.fields['department'].disabled = True



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
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'remarks']  # 包括备注字段
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3, 'placeholder': '输入备注说明'}),
            'employee': forms.TextInput(attrs={'readonly': 'readonly'}),  # 设置 employee 字段只读
            'date': forms.TextInput(attrs={'readonly': 'readonly'}),  # 设置 date 字段只读
        }