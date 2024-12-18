from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

# 注册视图
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # 保存用户
            login(request, user)  # 自动登录
            return redirect('home')  # 跳转到主页
    else:
        form = RegisterForm()
    return render(request, 'accounts_register.html', {'form': form})

# 登录视图
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # 登录用户
            position=user.employee.position
            if position == '普通员工' or position == '试用员工':
                return redirect('employee_list')  # 跳转到主页
            elif position =='组长':
                return redirect('employee_list')
            elif position == '部门经理':
                return redirect('employee_list') 
            elif position == '总经理':
                return redirect('employee_list')
    else:
        form = LoginForm()
    return render(request, 'accounts_login.html', {'form': form})

# 注销视图
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # 跳转到登录页
