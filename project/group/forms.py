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
class GroupFilterForm(forms.Form):
    id = forms.IntegerField(required=False, label='小组ID')
    name = forms.CharField(max_length=100, required=False, label='小组名称')
    department = forms.ChoiceField(choices=[('', '请选择')] + DEPARTMENT_CHOICES, required=False, label='部门')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 获取当前用户
        super().__init__(*args, **kwargs)

        if user and user.groups.filter(name='department_manager').exists():
            # 部门经理只能查看自己部门的小组
            self.fields['department'].disabled = True  # 禁用字段，不可编辑
            self.fields['department'].initial = user.employee.department  # 默认选择该部门
        if user and user.groups.filter(name='group_leader').exists():
            # 组长只能查看自己负责的小组
            self.fields['id'].disabled = True  # 禁用ID字段
            self.fields['name'].disabled = True  # 禁用名称字段
            self.fields['department'].disabled = True  # 禁用部门字段
            self.fields['department'].initial = user.employee.department  # 默认选中自己的部门
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
                # 使用 TextInput 显示部门名称，并使其不可编辑
                self.fields['department'].widget = TextInput(attrs={'value': current_department, 'readonly': 'readonly'})
                print("部门经理的部门是", current_department)

            except user.employee.DoesNotExist:
                print("没有找到对应的员工信息")

            
        
    def clean_members(self):
        members = self.cleaned_data.get('members')
        
        # 获取当前小组实例
        group = self.instance
        if group.pk:  # 确保小组已经存在并且是一个有效的小组实例
            # 检查小组当前成员数量
            current_member_count = group.members.count()
            
            # 如果现有成员数量与新添加的成员合计超过4个，抛出验证错误
            if current_member_count + len(members) > 4:
                raise ValidationError("每个小组最多只能有4名成员。")
        
        return members
class AddMemberForm(forms.Form):
    employee_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # 获取当前用户
        self.group = kwargs.pop('group', None)  # 获取当前小组
        super().__init__(*args, **kwargs)

        # 限制成员只能选择符合条件的员工
        employees = employee.objects.filter(position__in=['普通员工', '试用员工']).exclude(groups=self.group)
        self.fields['employee_id'].queryset = employees
        #将符合条件的员工填入ChoiceField的choices中
        self.fields['employee_id'].choices = [(emp.id, f"{emp.name} (ID: {emp.id})") for emp in employees]
            
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
            self.fields['leader'].queryset = group.members.filter(position__in=['普通员工', '试用员工', '员工组长'])
            
            
        self.fields['leader'].label_from_instance = self.get_leader_label
        
    def get_leader_label(self, member):
        return f"{member.name} (ID: {member.id})"  # 显示姓名和 ID
    def clean_leader(self):
        leader = self.cleaned_data.get('leader')

        # 如果选择了组长，且该成员的职位不符合要求，抛出验证错误
        if leader and leader.position not in ['普通员工', '试用员工', '员工组长']:
            raise forms.ValidationError(f"只有职位为 '普通员工'、'试用员工' 或 '员工组长' 的成员可以成为组长！")

        return leader
 