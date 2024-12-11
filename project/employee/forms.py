from django import forms
from .models import employee

class EmployeeFilterForm(forms.Form):
    SEX_CHOICES = [
        ('男', '男'),
        ('女', '女'),
    ]
    
    name = forms.CharField(max_length=100, required=False, label='姓名')
    sex = forms.ChoiceField(choices=SEX_CHOICES, required=False, label='性别')
    min_age = forms.IntegerField(required=False, label='最小年龄')
    max_age = forms.IntegerField(required=False, label='最大年龄')
    
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
    
    # 使用选择框选择性别
    sex = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.Select)
    
    # 使用日期选择控件
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2100)))

    class Meta:
        model = employee
        fields = ['id','name', 'sex', 'birthday', 'email', 'phone', 'address']

class EmployeeDeleteForm(forms.ModelForm):
    class Meta:
        model = employee
        fields = ['name', 'sex', 'birthday', 'email', 'phone', 'address']
        widgets = {
            'birthday': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让生日字段只读
            'sex': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让性别字段只读
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让姓名字段只读
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让邮箱字段只读
            'phone': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让电话字段只读
            'address': forms.TextInput(attrs={'readonly': 'readonly'}),  # 让地址字段只读
        }