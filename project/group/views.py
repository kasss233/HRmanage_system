from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group as user_Group
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from .models import Group
from .forms import GroupForm
from django.contrib.auth.decorators import user_passes_test
from employee.decorators import group_required
from django.views.generic import UpdateView
from django.views.generic import TemplateView
from django.views.generic import DetailView, View
from .forms import GroupFilterForm
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from .forms import AssignGroupLeaderForm
from django.contrib import messages
from .forms import GroupManagementForm
from .forms import AddMemberForm
from django.urls import reverse_lazy
from employee.models import employee
# Create your views here.
# views.py
# 权限控制函数，检查是否为总经理、部门经理或员工组长
def is_manager_or_leader(user):
    return user.is_authenticated and (
        user.profile.role in ['总经理', '部门经理', '员工组长']
    )
@method_decorator(group_required('department_manager', 'general_manager','group_leader'), name='dispatch')    
class GroupDetailView(DetailView):
    model = Group
    template_name = 'group_detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.object
        # 获取当前小组所有成员
        context['members'] = group.members.all()


        # 获取当前小组组长信息
        if group.leader:
            context['leader_name'] = group.leader.name
            context['leader_id'] = group.leader.id
        else:
            context['leader_name'] = None
            context['leader_id'] = None
            
       # 获取可以添加的成员：属于当前小组部门且为普通员工或试用员工
        # 首先，检查小组是否有部门，防止获取 `None` 的部门
        if group.department:
            available_employees = employee.objects.filter(
                position__in=['普通员工', '试用员工'],
                department=group.department
            ).exclude(groups=group)  # 排除当前小组成员
        else:
            available_employees = employee.objects.none()  # 如果没有部门，返回空的查询集
        
        # 如果传递了员工ID进行过滤
        employee_id_filter = self.request.GET.get('employee_id_filter', None)
        if employee_id_filter:
            available_employees = available_employees.filter(id=employee_id_filter)

        context['available_employees'] = available_employees
        return context
    def post(self, request, *args, **kwargs):
        group = self.get_object()
        employee_id = request.POST.get('employee_id')
        action = request.POST.get('action')

        if action == 'add_member' and employee_id:
            try:
                employees = employee.objects.get(id=employee_id)
                if group.members.count() < 4:  # 判断小组成员是否少于 4
                    group.members.add(employees)
                    messages.success(request, f"{employees.name} 已成功添加到小组。")
                else:
                    messages.error(request, "小组成员已满，最多只能有 4 名成员。")
            except employee.DoesNotExist:
                messages.error(request, "未找到该员工。")
        elif action == 'remove_member' and employee_id:
            try:
                employee_to_remove = employee.objects.get(id=employee_id)
                # 如果被删除的是组长，执行特殊操作
                 # 检查是否是组长，若是组长则不可删除
                if group.leader == employee_to_remove:
                    messages.error(request, "小组组长不能被删除。")
                else:
                    group.members.remove(employee_to_remove)
                    messages.success(request, f"{employee_to_remove.name} 已从小组中移除。")
            except employee.DoesNotExist:
                messages.error(request, "未找到该员工。")
            except ValueError:
                messages.error(request, "员工 ID 必须是一个有效的整数。")
        
        return redirect('group_detail', pk=group.id)  # 刷新页面，显示更新后的成员列表
@method_decorator(group_required('department_manager', 'general_manager','group_leader'), name='dispatch')
class AddMemberToGroupView(UpdateView):
    model = Group
    form_class = AddMemberForm
    template_name = 'add_member_to_group.html'
    success_url = reverse_lazy('group_management')  # 成功后跳转到小组列表页面

    def post(self, request, group_id):
        group = Group.objects.get(id=group_id)
        employee_id = request.POST.get('employee_id')

        try:
            member = employee.objects.get(id=employee_id)

            # 判断该员工是否符合可添加条件
            if member.department == group.department and member.position in ['普通员工', '试用员工']:
                if group.members.count() < 4:  # 判断小组成员是否少于 4 人
                    group.members.add(member)
                    messages.success(request, f"{member.name} 已成功添加到小组。")
                else:
                    messages.error(request, "小组成员已满，最多只能有 4 名成员。")
            else:
                messages.error(request, "该员工不符合添加条件。")

        except employee.DoesNotExist:
            messages.error(request, "未找到该员工。")

        return redirect('group_detail', pk=group.id)  # 跳转到小组详情页面
@method_decorator(group_required('department_manager', 'general_manager'), name='dispatch')   
class RemoveMemberFromGroupView(View):
    def post(self, request, group_id, employee_id):
        # 获取当前小组和员工
        group = get_object_or_404(Group, id=group_id)
        member = get_object_or_404(employee, id=employee_id)

        # 检查当前用户是否有权限删除该成员
        if not group.members.filter(id=member.id).exists():
            return HttpResponseForbidden("您不能删除该成员。")

        # 从小组中移除该成员
        group.members.remove(member)

        # 重新定向到当前小组页面或其他相关页面
        return redirect('group_detail', pk=group.id)  # 跳转到小组详情页面
@method_decorator(group_required('department_manager', 'general_manager'), name='dispatch')
class AssignGroupLeaderView(UpdateView):
    model = Group
    template_name = 'assign_group_leader.html'
    form_class = AssignGroupLeaderForm  # 使用自定义的表单
    success_url = reverse_lazy('group_management')  # 成功后跳转到小组列表页面
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.get_object()  # 获取当前小组实例
        context['group'] = group  # 将小组传递给模板
        context['user'] = self.request.user  # 将当前用户传递给模板
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user  # 获取当前用户
        group = self.get_object()  # 获取当前小组实例
        kwargs['user'] = user  # 将用户信息传递给表单的 __init__ 方法
        kwargs['group'] = group  # 将小组实例传递给表单
        return kwargs


    def form_valid(self, form):
        # 获取表单数据
        group = self.get_object()
        new_leader = form.cleaned_data['leader']
        
        # 如果没有选择组长，直接跳过
        if not new_leader:
            return redirect(self.success_url)
        
        # 确保新的组长成员属于该小组
        if new_leader not in group.members.all():
            form.add_error('leader', '新的组长必须是该小组的成员！')
            return self.form_invalid(form)
        
        # 如果当前组长不同于新组长，则将原组长的职位设置为普通员工
        if group.leader and group.leader != new_leader:
            # 将原组长的职位改为 "普通员工"
            group.leader.position = '普通员工'
            group.leader.user.groups.remove(user_Group.objects.get(name='group_leader'))  # 移除员工组长角色
            group.leader.user.groups.add(user_Group.objects.get(name='employee'))  # 添加普通员工角色
            group.leader.save()

        # 更新小组的组长
        group.leader = new_leader
        group.save()

        # 更新新的组长的职位为 "员工组长"
        new_leader.position = '员工组长'
        if new_leader.user.groups.filter(name='employee').exists():
            new_leader.user.groups.remove(user_Group.objects.get(name='employee'))  # 移除普通员工角色
            new_leader.user.groups.add(user_Group.objects.get(name='group_leader'))  # 添加员工组长角色
        new_leader.save()

        # 重定向到小组列表页面
        return redirect(self.success_url)  # 不传递 pk
@method_decorator(group_required('department_manager', 'general_manager'), name='dispatch')
class RevokeGroupLeaderView(View):
    def post(self, request, group_id):
        # 获取小组实例
        group = get_object_or_404(Group, id=group_id)

        if group.leader:
            # 获取当前组长
            old_leader = group.leader

            # 撤销组长，将组长设为 None
            group.leader = None
            group.save()

            # 将原组长的职位设置为 "普通员工"
            old_leader.position = '普通员工'
            old_leader.user.groups.remove(user_Group.objects.get(name='group_leader'))  # 移除员工组长角色
            old_leader.user.groups.add(user_Group.objects.get(name='employee'))  # 添加普通员工角色
            old_leader.save()

            messages.success(request, f"成功撤销 {old_leader.name} 的组长职位！")
        else:
            messages.warning(request, "该小组没有组长，无需撤销。")

        return redirect('group_management')  # 重定向到小组管理页面或其他合适的页面

@method_decorator(group_required('department_manager', 'general_manager'), name='dispatch')
class CreateGroupView(CreateView):
    model = Group  # 这是你的Group模型
    template_name = 'create_group.html'  # 模板文件
    form_class = GroupForm  # 小组创建表单类
    success_url = reverse_lazy('group_management')  # 创建成功后跳转到小组列表页面

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
        
        return self.render_to_response(self.get_context_data(result=result_message))

    def form_invalid(self, form):
        # 表单验证失败时的处理
        print("表单验证失败:", form.errors)
        result_message = "表单验证失败，请检查填写的内容。"
        return self.render_to_response(self.get_context_data(result=result_message))
    
@method_decorator(group_required('department_manager', 'general_manager','group_leader'), name='dispatch')    
class GroupManagementView(TemplateView):
    template_name = 'group_management.html'
    
    def get(self, request, *args, **kwargs):
        # 获取筛选表单并进行过滤
        form = GroupFilterForm(request.GET, user=request.user)  # 提供当前用户信息
        groups = Group.objects.all()  # 默认获取所有小组
        
        if form.is_valid():
            # 根据表单字段进行筛选
            group_id = form.cleaned_data.get('id')
            group_name = form.cleaned_data.get('name')
            department = form.cleaned_data.get('department')

            if group_id:
                groups = groups.filter(id=group_id)
            if group_name:
                groups = groups.filter(name__icontains=group_name)
            if department:
                groups = groups.filter(department=department)

        # 将筛选结果传递给模板
        context = {
            'form': form,
            'groups': groups
        }
        return self.render_to_response(context)
@method_decorator(group_required('department_manager', 'general_manager'), name='dispatch')
class DeleteGroupView(View):
    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        return render(request, 'delete_group.html', {'group': group})
    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        

        # 获取当前用户
        user = request.user

        # 部门经理只能删除自己部门的小组
        if user.groups.filter(name='department_manager').exists():
            # 获取部门经理所属的员工
            employees = get_object_or_404(employee, user=user)
            if group.department != employees.department:
                messages.error(request, "您只能删除自己部门的小组！")
                return redirect('group_management')

        # 员工组长只能删除自己的小组
        elif user.groups.filter(name='group_leader').exists():
            # 获取员工组长的小组
            employees = get_object_or_404(employee, user=user)
            if group not in employee.groups.all():
                messages.error(request, "您只能删除您所在的小组！")
                return redirect('group_management')

        # 如果是其他角色，允许删除任何小组
        elif user.groups.filter(name='general_manager').exists():
            pass  # 总经理可以删除任何小组

        else:
            messages.error(request, "您没有权限删除小组！")
            return redirect('group_management')
     # 在删除小组之前，将组长的职位改为普通员工
        if group.leader:  # 假设每个小组都有一个 leader（组长）
            leader = group.leader
            leader.position = '普通员工'  # 将职位改为普通员工
            leader.user.groups.remove(user_Group.objects.get(name='group_leader'))
            leader.user.groups.add(user_Group.objects.get(name='employee'))
            leader.save()
        # 如果权限通过，删除小组
        
        group.delete()

        # 提示删除成功
        messages.success(request, f"小组 '{group.name}' 删除成功！")
        return redirect('group_management')