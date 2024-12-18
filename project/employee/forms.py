from django import forms
from .models import employee

class EmployeeFilterForm(forms.Form):
    SEX_CHOICES = [
        ('男', '男'),
        ('女', '女'),
    ]
    
    name = forms.CharField(max_length=100, required=False, label='姓名')
    sex = forms.ChoiceField(choices=SEX_CHOICES, required=False, label='性别')
    
    # 使用 SelectDateWidget 来选择生日日期（注意，birthday 这里不应该是单独的选择字段，而是通过 datepicker 提供）
    birthday = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(years=range(1900, 2100)),
        label='出生日期'
    )


class EmployeeForm(forms.ModelForm):
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
    # 使用选择框选择性别
    sex = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.Select)
    
    # 使用日期选择控件
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)))
    position = forms.ChoiceField(choices=POSITION_CHOICES, widget=forms.Select)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select)
    class Meta:
        model = employee
        fields = ['id','name', 'sex', 'birthday', 'email', 'phone', 'address','department','position']

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
        }