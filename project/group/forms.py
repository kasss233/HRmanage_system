# forms.py
from django import forms
from django.forms.widgets import TextInput
from .models import Group
from django.apps import apps
from employee.models import employee
from django.core.exceptions import ValidationError

class GroupForm(forms.ModelForm):
    # 如果你需要定义小组名称等字段，可以添加自定义选择项
    # 此处示例没有添加额外的选择项，因为字段都比较简单
    class Meta:
        model = Group
        fields = ['name', 'department', 'leader']# 假设 Group 模型有这些字段

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 获取当前用户
        super().__init__(*args, **kwargs)
        
        
        Employee = apps.get_model('employee', 'Employee')
        self.fields['leader'].queryset = Employee.objects.all()
 
        # 如果当前用户是部门经理，限制部门选择为当前用户所属的部门
        if user and user.groups.filter(name='department_manager').exists():
            try:
                employee_obj = user.employee  # 假设你已经为用户关联了员工对象
                current_department = employee_obj.department  # 获取当前部门
                # 将 department 字段设置为只读，并默认选中当前部门
                self.fields['department'].initial = current_department
                # 限制 department 字段的选择项为当前部门
                self.fields['department'].choices = [(current_department, current_department)]
                # 禁用部门选择字段
                self.fields['department'].disabled = True  # 禁用字段，不可编辑
                # 使用 TextInput 显示部门名称，并使其不可编辑
                self.fields['department'].widget = TextInput(attrs={'value': current_department, 'readonly': 'readonly'})
                print("部门经理的部门是", current_department)

                # 如果是部门经理，限制可选领导为当前部门的员工
                self.fields['leader'].queryset = self.fields['leader'].queryset.filter(department=current_department)

                # 如果是部门经理，限制只能选择"员工"或"员工组长"等职位
                #self.fields['position'].choices = [
                    #('普通员工', '普通员工'),
                    #('员工组长', '员工组长'),
                    #('试用员工', '试用员工')
                #]

            except user.employee.DoesNotExist:
                print("没有找到对应的员工信息")
        elif user and user.groups.filter(name='general_manager').exists():
            # 如果是总经理，允许选择任何部门和任何领导
            self.fields['leader'].queryset = self.fields['leader'].queryset.all()  # 不做任何限制
            self.fields['department'].disabled = False  # 总经理可以选择任何部门
            # 如果是总经理，允许选择所有职位
            #self.fields['position'].choices = [
                #('试用员工', '试用员工'),
                #('普通员工', '普通员工'),
                #('员工组长', '员工组长'),
                #('部门经理', '部门经理'),
                #('总经理', '总经理')
            #]
        else:
            # 如果不是部门经理或总经理，可以根据需要调整
            self.fields['leader'].queryset = self.fields['leader'].queryset.none()  # 不允许选择任何领导
            self.fields['department'].disabled = True  # 禁用部门字段
            #self.fields['position'].disabled = True  # 禁用职位字段
        def clean_name(self):
            name = self.cleaned_data.get('name')
        
            # 判断小组名称是否已存在
            if Group.objects.filter(name=name).exists():
                raise ValidationError(f"小组名称 '{name}' 已经存在，请选择其他名称。")
        
            return name
            
class AddMemberForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['members']  # 选择成员

    members = forms.ModelMultipleChoiceField(
        queryset=employee.objects.all(),  # 默认展示所有员工
        widget=forms.CheckboxSelectMultiple,  # 使用复选框展示
        required=False  # 允许没有选择成员
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 获取当前用户
        super().__init__(*args, **kwargs)

        # 根据当前用户的角色限制成员选择
        if user and user.groups.filter(name='department_manager').exists():
            # 部门经理只能看到自己部门的员工
            employees = employee.objects.get(user=user)
            self.fields['members'].queryset = employee.objects.filter(department=employees.department)

        elif user and user.groups.filter(name='group_leader').exists():
            # 员工组长只能看到自己小组的成员
            employees = employee.objects.get(user=user)
            self.fields['members'].queryset = employees.groups.all().first().members.all()

        elif user and user.groups.filter(name='general_manager').exists():
            # 总经理可以看到所有员工
            self.fields['members'].queryset = employee.objects.all()
            
class AssignGroupLeaderForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['leader']  # 只允许选择新的组长

    leader = forms.ModelChoiceField(queryset=employee.objects.all())  # 选择新组长

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 获取当前用户
        super().__init__(*args, **kwargs)

        if user and user.groups.filter(name='department_manager').exists():
            employees = employee.objects.get(user=user)
            self.fields['leader'].queryset = employee.objects.filter(department=employees.department)

        elif user and user.groups.filter(name='general_manager').exists():
            self.fields['leader'].queryset = employee.objects.all()