from django import forms
from .models import employee
from django.forms.widgets import TextInput
from .models import group
class EmployeeFilterForm(forms.Form):
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
    
    # 表单字段
    name = forms.CharField(max_length=100, required=False, label='姓名')
    sex = forms.ChoiceField(choices=SEX_CHOICES, required=False, label='性别')
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, required=False, label='部门')
    birthday = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(years=range(1900, 2100)),
        label='出生日期'
    )
    group = forms.ModelChoiceField(
        queryset=group.objects.all(),  # 初始查询所有小组
        required=False,
        label='小组',
        empty_label="选择小组"
    )
    

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 获取当前用户
        super().__init__(*args, **kwargs)

        if user:
            if user.groups.filter(name='department_manager').exists():  # 部门经理
                try:
                    employee_obj = employee.objects.get(user=user)
                    current_department = employee_obj.department  # 获取当前部门
                    
                    # 限制部门选择为当前部门
                    self.fields['department'].initial = current_department
                    self.fields['department'].choices = [(current_department, current_department)]
                    self.fields['department'].disabled = True  # 禁用部门字段
                    
                    # 根据部门筛选小组
                    self.fields['group'].queryset = group.objects.filter(department=current_department)

                except employee.DoesNotExist:
                    print("没有找到对应的员工信息")
            elif user.groups.filter(name='team_leader').exists():  # 组长
                try:
                    employee_obj = employee.objects.get(user=user)
                    current_group = employee_obj.group  # 获取当前小组
                    current_department = employee_obj.department  # 获取当前部门

                    # 限制部门和小组选择为当前组长所属的小组
                    self.fields['department'].initial = current_department
                    self.fields['department'].choices = [(current_department, current_department)]
                    self.fields['department'].disabled = True  # 禁用部门字段

                    self.fields['group'].initial = current_group
                    self.fields['group'].choices = [(current_group.id, current_group.name)]  # 仅显示当前小组
                    self.fields['group'].disabled = True  # 禁用小组字段



                except employee.DoesNotExist:
                    print("没有找到对应的员工信息")
            else:  # 总经理
                # 总经理可以查看所有小组成员
                self.fields['employee_member'].queryset = employee.objects.all()
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
    # 使用 ModelChoiceField 动态加载小组
    group = forms.ModelChoiceField(
        queryset=group.objects.none(),  # 默认不显示任何小组
        required=False,
        label="小组",
        empty_label="请选择小组"
    )
    class Meta:
        model = employee
        fields = ['id','name', 'sex', 'birthday', 'email', 'phone', 'address','department','position','group']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 获取当前用户
        super().__init__(*args, **kwargs)
        # 如果当前用户是部门经理，限制部门选择为当前用户所属的部门
        if user and user.groups.filter(name='department_manager').exists():
            try:
                employee_obj = employee.objects.get(user=user)
                current_department = user.employee.department  # 获取当前部门
                # 将 department 字段设置为只读，并默认选中当前部门
                self.fields['department'].initial = current_department
                # 限制 department 字段的选择项为当前部门
                self.fields['department'].choices = [(current_department, current_department)]
                # 禁用部门选择字段
                self.fields['department'].disabled = True  # 禁用字段，不可编辑
                # 使用 TextInput 显示部门名称，并使其不可编辑
                self.fields['department'].widget = TextInput(attrs={'value': current_department, 'readonly': 'readonly'})
                 # 限制 group 字段的选择项为当前部门下的所有小组
                self.fields['group'].queryset = group.objects.filter(department=current_department)
                print("部门经理的部门是", current_department)
                new_position_choices = [choice for choice in self.POSITION_CHOICES if choice[0] not in ['部门经理', '总经理']]
                self.fields['position'].choices = new_position_choices  # 更新 position 选择项
            except employee.DoesNotExist:
                print("没有找到对应的员工信息")

class CreateGroupsForm(forms.Form):
    # 部门选项可以作为类变量来定义
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
    
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, label="部门")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        current_department = kwargs.pop('current_department', None)
        super().__init__(*args, **kwargs)

        # 调整部门字段选择项
        self._adjust_department_choices(user, current_department)

    def _adjust_department_choices(self, user, current_department):
        """根据用户角色调整部门选择"""
        if user and user.groups.filter(name='manager').exists():
            # 总经理可以选择任何部门
            self.fields['department'].choices = self.DEPARTMENT_CHOICES
        elif user and user.groups.filter(name='department_manager').exists():
            # 部门经理只能选择当前部门
            if current_department:
                self.fields['department'].initial = current_department
                self.fields['department'].widget = forms.HiddenInput()
                self.fields['department'].choices = [(current_department, current_department)]
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