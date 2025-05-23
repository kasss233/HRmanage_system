from django import forms
from .models import employee
from django.forms.widgets import TextInput
SEX_CHOICES = [
        ('男', '男'),
        ('女', '女'),
    ]
POSITION_CHOICES = [
        ('试用员工', '试用员工'),
        ('普通员工', '普通员工'),
        ('员工组长', '员工组长'),
        ('总经理', '总经理'),
        ('部门经理', '部门经理'),
    ]
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
class EmployeeFilterForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label='姓名')
    sex = forms.ChoiceField(choices=SEX_CHOICES, required=False, label='性别')
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES,required=False, label='部门')
    group=forms.CharField(max_length=100,required=False,label='小组')
    birthday = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(years=range(1900, 2100)),
        label='出生日期'
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 获取当前用户
        super().__init__(*args, **kwargs)
        if user.groups.filter(name='department_manager').exists():  # 判断是否为部门经理
            self.fields['department'].disabled = True  # 禁用字段，不可编辑
        elif user.groups.filter(name='group_leader').exists():
            self.fields['group'].disabled = True  # 禁用字段，不可编辑
            self.fields['department'].disabled = True  # 禁用字段，不可编辑

class EmployeeForm(forms.ModelForm):
    name=forms.CharField(max_length=100,label='姓名')
    sex = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.Select,label='性别')
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)),label='出生日期')
    email = forms.EmailField(label='邮箱')
    phone = forms.CharField(max_length=11, label='电话')
    address = forms.CharField(max_length=100, label='地址')
    position = forms.ChoiceField(choices=POSITION_CHOICES, widget=forms.Select,label='职位')
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select,label='部门')
    details=forms.CharField(widget=forms.Textarea,required=False,label='培训技能')
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 获取当前用户
        super().__init__(*args, **kwargs)
        if user.groups.filter(name='department_manager').exists():
            employee_obj = employee.objects.get(user=user)
            current_department = user.employee.department  # 获取当前部门
            self.fields['department'].widget = TextInput(attrs={'value': current_department, 'readonly': 'readonly'})
            self.fields['department'].choices = [(current_department, current_department)]  # 更新 department 选择项
            new_position_choices = [choice for choice in POSITION_CHOICES if choice[0] not in ['部门经理', '总经理']]
            self.fields['position'].choices = new_position_choices  # 更新 position 选择项
        elif user.groups.filter(name='group_leader').exists():
            employee_obj = employee.objects.get(user=user)
            current_department = user.employee.department  # 获取当前部门
            self.fields['department'].widget = TextInput(attrs={'value': current_department, 'readonly': 'readonly'})
            self.fields['department'].choices = [(current_department, current_department)]  # 更新 department 选择项
            new_position_choices = [choice for choice in POSITION_CHOICES if choice[0] not in ['部门经理', '总经理','员工组长']]
            self.fields['position'].choices = new_position_choices  # 更新 position 选择项
    class Meta:
        model = employee
        fields = ['id','name', 'sex', 'birthday', 'email', 'phone', 'address','department','position','details']
        
class EmployeeDeleteForm(forms.ModelForm):
    class Meta:
        model = employee
        fields = ['id','name', 'sex', 'birthday', 'email', 'phone', 'address','department','position']
        widgets = {
            'birthday': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让生日字段只读
            'sex': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让性别字段只读
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让姓名字段只读
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让邮箱字段只读
            'phone': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让电话字段只读
            'address': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让地址字段只读
            'department': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让部门字段只读
            'position': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让职位字段只读
            'group': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让小组字段只读
        }