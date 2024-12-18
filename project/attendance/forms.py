from django import forms
from .models import Attendance
from employee.models import employee

class AttendanceFilterForm(forms.Form):
    # 添加姓名搜索框
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

    # 提供筛选的默认值
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = employee.objects.all()

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
