from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.utils.decorators import method_decorator
from .models import Group
from .forms import GroupForm
from .decorators import group_required
from django.views.generic import UpdateView
from .forms import AddMemberForm
from django.urls import reverse_lazy
from employee.models import employee
# Create your views here.
# views.py

class AddMemberToGroupView(UpdateView):
    model = Group
    form_class = AddMemberForm
    template_name = 'group/add_member_to_group.html'
    success_url = reverse_lazy('group_list')  # 成功后跳转到小组列表页面

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.object  # 获取当前小组对象
        context['user_role'] = self.request.user.groups.first().name  # 获取当前用户的角色
        return context

    def get_form_kwargs(self):
        # 获取当前用户
        kwargs = super().get_form_kwargs()
        user = self.request.user

        # 获取小组对象
        group = self.get_object()

        # 如果是部门经理，限制只能看到自己部门的员工
        if user.groups.filter(name='department_manager').exists():
            # 获取部门经理所在的部门
            employees = employee.objects.get(user=user)
            department = employees.department
            kwargs['queryset'] = employee.objects.filter(department=department)

        # 如果是员工组长，限制只能看到自己小组的成员
        elif user.groups.filter(name='group_leader').exists():
            # 获取员工组长所在的小组
            group_leader = employee.objects.get(user=user)
            groups = group_leader.groups.all()
            kwargs['queryset'] = employee.objects.filter(groups__in=groups)

        # 总经理可以管理任何部门的员工
        elif user.groups.filter(name='general_manager').exists():
            kwargs['queryset'] = employee.objects.all()

        return kwargs

    def form_valid(self, form):
        # 在提交表单前，确保所有被添加的成员都在相同部门
        group = self.get_object()
        for member in form.cleaned_data['members']:
            if member.department != group.department:
                form.add_error('members', f"员工 {member.name} 不属于该小组所属的部门！")
                return self.form_invalid(form)

        return super().form_valid(form)


class AssignGroupLeaderView(UpdateView):
    model = Group
    template_name = 'group/assign_group_leader.html'
    fields = ['leader']  # 选择组长

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.groups.first().name  # 获取当前用户的角色
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user

        # 如果是部门经理，只能看到自己部门的员工
        if user.groups.filter(name='department_manager').exists():
            employees = employee.objects.get(user=user)
            department = employees.department
            kwargs['queryset'] = employee.objects.filter(department=department)
        
        # 如果是总经理，可以选择所有员工
        elif user.groups.filter(name='general_manager').exists():
            kwargs['queryset'] = employee.objects.all()

        return kwargs

    def form_valid(self, form):
        # 获取表单数据
        group = self.get_object()
        new_leader = form.cleaned_data['leader']

        # 确保新的组长成员属于该小组
        if new_leader not in group.members.all():
            form.add_error('leader', '新的组长必须是该小组的成员！')
            return self.form_invalid(form)

        # 更新小组的组长
        group.leader = new_leader
        group.save()

        return redirect(reverse_lazy('group_detail', kwargs={'pk': group.pk}))

@method_decorator(group_required('department_manager', 'general_manager'), name='dispatch')
class CreateGroupView(CreateView):
    model = Group  # 这是你的Group模型
    template_name = 'group_create.html'  # 模板文件
    form_class = GroupForm  # 小组创建表单类
    success_url = reverse_lazy('group_list')  # 创建成功后跳转到小组列表页面

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GroupForm(self.request.GET, user=self.request.user)
        context['is_manager'] = self.request.user.groups.filter(name='general_manager').exists()
        context['is_department_manager'] = self.request.user.groups.filter(name='department_manager').exists()
        context['is_group_leader'] = self.request.user.groups.filter(name='group_leader').exists()
        return context

    def form_valid(self, form):
        # 在表单有效时，处理小组的创建
        group = form.save(commit=False)  # 保存小组
         # 如果是总经理，可以更换部门
        if self.request.user.groups.filter(name='general_manager').exists():
            department = form.cleaned_data['department']
            group.department = department
            
        group.save()  # 保存小组
        group_name = group.name
        result_message = f"小组'{group_name}'创建成功！"
        
         # 如果是部门经理，限制只能创建自己部门的小组
        if self.request.user.groups.filter(name='department_manager').exists():
            employee_obj = self.request.user.employee
            current_department = employee_obj.department
            if group.department != current_department:
                result_message = "您只能创建属于您部门的小组！"
                group.delete()
                return self.render_to_response(self.get_context_data(result=result_message))
        
      # 如果是员工组长，限制只能创建自己部门的小组
        if self.request.user.groups.filter(name='group_leader').exists():
            employee_obj = self.request.user.employee
            current_department = employee_obj.department
            if group.department != current_department:
                result_message = "您只能创建属于您部门的小组！"
                group.delete()
                return self.render_to_response(self.get_context_data(result=result_message))
        
        return self.render_to_response(self.get_context_data(result=result_message))