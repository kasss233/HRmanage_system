# 人力资源管理系统

## 项目简介

本项目是一个基于 Django 框架开发的人力资源管理系统，旨在帮助企业高效管理员工信息、考勤记录、工资发放以及小组管理等功能。系统支持多角色权限控制（如普通员工、部门经理、总经理等），并提供直观的用户界面，提升用户体验。

---

## 功能模块

### 1. 员工管理

- 添加、更新、删除员工信息。
- 查看员工详细信息。
- 支持员工筛选和分页功能。

### 2. 小组管理

- 创建、更新、删除小组。
- 为小组分配组长。
- 管理小组成员。

### 3. 考勤管理

- 员工签到、签退功能。
- 查看考勤记录，支持筛选和分页。
- 自动计算迟到、早退、缺勤次数。

### 4. 工资管理

- 设置工资标准（基本工资、迟到扣款、缺勤扣款、全勤奖等）。
- 自动计算员工工资（包括奖金、扣款等）。
- 支持工资发放状态管理。

### 5. 用户权限管理

- 基于 Django 的用户组和权限系统，限制不同角色的操作范围。
- 普通员工、部门经理、总经理拥有不同的权限。

---

## 技术栈

- **后端**: Django 5.1.4
- **数据库**: MySQL
- **前端**: HTML、CSS（Bootstrap）、JavaScript
- **环境**: Python 3.12

---

## 安装与运行

### 1. 克隆项目

```bash
git clone https://github.com/your-repo/hr-management-system.git
cd hr_management_system
python -m venv .venv
.venv\Scripts\activate
pip install -r [requirements.txt](http://_vscodecontentref_/0)
```

在 settings.py 中修改数据库配置（默认使用sqlite）：

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "your_database_name",
        "USER": "your_username",
        "PASSWORD": "your_password",
        "HOST": "your_host",
        "PORT": "your_port",
    }
}
```

运行迁移

```
python manage.py makemigrations
python manage.py migrate
```

启动开发服务器

```
python manage.py runserver
```

使用默认总经理账号：1密码：1进行登录
