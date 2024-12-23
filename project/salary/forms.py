from django import forms
from .models import Salary


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['bonus']  # 只关注奖金字段

    def __init__(self, *args, **kwargs):
        # 确保可以通过传递当前的 employee 对象进行初始化
        self.employee = kwargs.get('employee', None)
        super(SalaryForm, self).__init__(*args, **kwargs)

        # 初始化 bonus 字段的默认值
        if self.employee:
            self.initial['bonus'] = self.employee.salary.bonus if self.employee.salary else 0.00
