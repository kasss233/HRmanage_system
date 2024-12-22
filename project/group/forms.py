# forms.py
from django import forms
from django.forms.widgets import TextInput
from .models import Group
from django.apps import apps
from employee.models import employee
from django.core.exceptions import ValidationError
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

class GroupManagementForm(forms.Form):
    # 这个表单用于展示小组信息并包含操作按钮
    group_name = forms.IntegerField(widget=forms.HiddenInput())
    add_member_button = forms.CharField(widget=forms.HiddenInput(), required=False)
    assign_leader_button = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class GroupForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select)
    class Meta:
        model = Group
        fields = ['name', 'department']# 假设 Group 模型有这些字段

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 获取当前用户
        super().__init__(*args, **kwargs)
        
        
        Employee = apps.get_model('employee', 'Employee')
 
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

            except user.employee.DoesNotExist:
                print("没有找到对应的员工信息")
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
        queryset=employee.objects.filter(position__in=['普通员工', '实习员工','员工组长']),  # 只显示普通员工、实习员工
        widget=forms.CheckboxSelectMultiple,  # 使用复选框展示
        required=False  # 允许没有选择成员
    )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 获取当前用户
        group = kwargs.pop('group', None)  # 获取当前小组实例
        super().__init__(*args, **kwargs)
        
        self.fields['members'].queryset=group.members.filter(position__in=['普通员工', '实习员工','员工组长'])
        
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

        # 修改成员的显示方式：姓名 + 部门+ 小组
        self.fields['members'].label_from_instance = self.get_member_label
        
       

    def clean_members(self):
        selected_members = self.cleaned_data['members']
        group = self.instance  # 当前小组实例

        # 检查所选成员是否已属于其他小组
        for member in selected_members:
            # 如果成员已经在其他小组中，并且不是当前小组的成员，抛出验证错误
            if member.groups.exclude(id=group.id).exists():  # 排除当前小组，检查是否属于其他小组
                raise ValidationError(f"{member.name} 已是其他小组的成员，无法重复添加。")
        return selected_members

    def get_member_label(self, obj):
        """
        定制成员显示标签格式：姓名 + 部门 + 小组
        """
        return f"{obj.name} + {obj.department} + {obj.groups.first() if obj.groups.exists() else '未分配小组'}"
            
class AssignGroupLeaderForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['leader']  # 只允许选择新的组长

    leader = forms.ModelChoiceField(
        queryset=employee.objects.all(),  # 选择组长的成员
        required=False  # 使得 leader 字段可以为空
    )

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)  # 获取当前小组实例
        user = kwargs.pop('user', None)  # 获取当前用户
        super().__init__(*args, **kwargs)
        
        if group:
            # 限制组长选择范围，只能选择该小组的成员，并且职位为普通员工、实习员工、员工组长
            self.fields['leader'].queryset = group.members.filter(position__in=['普通员工', '实习员工', '员工组长'])
            
            
        self.fields['leader'].label_from_instance = self.get_leader_label
        
    def get_leader_label(self, member):
        return f"{member.name} (ID: {member.id})"  # 显示姓名和 ID
    def clean_leader(self):
        leader = self.cleaned_data.get('leader')

        # 如果选择了组长，且该成员的职位不符合要求，抛出验证错误
        if leader and leader.position not in ['普通员工', '实习员工', '员工组长']:
            raise forms.ValidationError(f"只有职位为 '普通员工'、'实习员工' 或 '员工组长' 的成员可以成为组长！")

        return leader
 