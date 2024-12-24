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
            return redirect('employee_frontpage')
    else:
        form = LoginForm()
    return render(request, 'accounts_login.html', {'form': form})

# 注销视图
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # 跳转到登录页

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SimplePasswordResetForm

@login_required
def reset_password(request):
    is_employee = request.user.groups.filter(name='employee').exists()
    if request.method == "POST":
        form = SimplePasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "密码重置成功！请重新登录。")
            return redirect("login")  # 重定向到登录页面
    else:
        form = SimplePasswordResetForm()
    return render(request, "reset_password.html", {"form": form,
                                                  "is_employee": is_employee})

