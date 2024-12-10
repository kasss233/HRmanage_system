from django import forms
from .models import employee

class EmployeeFilterForm(forms.Form):
    SEX_CHOICES = [
        ('男', '男'),
        ('女', '女'),
    ]
    
    name = forms.CharField(max_length=100, required=False, label='Name')
    sex = forms.ChoiceField(choices=SEX_CHOICES, required=False, label='Sex')
    min_age = forms.IntegerField(required=False, label='Min Age')
    max_age = forms.IntegerField(required=False, label='Max Age')
    
    # 使用 SelectDateWidget 来选择生日日期（注意，birthday 这里不应该是单独的选择字段，而是通过 datepicker 提供）
    birthday = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(years=range(1900, 2100)),
        label='Birthday'
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
