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


    
class EmployeeForm(forms.ModelForm):
    SEX_CHOICES = [
        ('男', '男'),
        ('女', '女'),
    ]
    
    sex = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.Select)  # 使用选择框选择性别
    
    # 使用HTML5的日期输入控件
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1900, 2100))  # 提供日期选择框
    )

    class Meta:
        model = employee
        fields = ['name', 'sex', 'birthday', 'email', 'phone', 'address']