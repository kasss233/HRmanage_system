在 Django 项目中，可以通过扩展模型和表单功能来记录员工的能力、培训经历和工作经验。以下是具体实现步骤，包括数据库设计、表单设计以及模板展示。

---

### 1. 扩展 `employee` 模型
在 `employee/models.py` 中，添加以下字段记录员工的详细档案信息：

```python
from django.db import models

class Employee(models.Model):
    # 原有字段
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=2, choices=[('男', '男'), ('女', '女')])
    birthday = models.DateField()
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    # 新增字段
    abilities = models.TextField(blank=True, null=True, verbose_name="能力")
    training_experiences = models.TextField(blank=True, null=True, verbose_name="培训经历")
    work_experiences = models.TextField(blank=True, null=True, verbose_name="工作经验")

    def __str__(self):
        return self.name
```

#### 字段说明：
- **`abilities`**：用于记录员工的技能或能力，可以是较长文本。
- **`training_experiences`**：记录员工的培训经历。
- **`work_experiences`**：记录员工的工作经验。

---

### 2. 数据迁移
添加字段后，执行以下命令更新数据库：
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 3. 创建表单
在 `employee/forms.py` 中创建一个表单类，用于处理员工档案的输入：

```python
from django import forms
from .models import Employee

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['abilities', 'training_experiences', 'work_experiences']
        widgets = {
            'abilities': forms.Textarea(attrs={'rows': 5, 'placeholder': '请输入员工的能力描述'}),
            'training_experiences': forms.Textarea(attrs={'rows': 5, 'placeholder': '请输入员工的培训经历'}),
            'work_experiences': forms.Textarea(attrs={'rows': 5, 'placeholder': '请输入员工的工作经验'}),
        }
        labels = {
            'abilities': '能力',
            'training_experiences': '培训经历',
            'work_experiences': '工作经验',
        }
```

---

### 4. 创建或更新视图
在 `employee/views.py` 中添加用于显示和更新员工档案的视图：

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from .forms import EmployeeProfileForm

def employee_profile_view(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')  # 更新后跳转到员工列表页
    else:
        form = EmployeeProfileForm(instance=employee)

    return render(request, 'employee_profile.html', {'form': form, 'employee': employee})
```

---

### 5. 创建模板
在 `templates/employee_profile.html` 中，添加一个用于展示和编辑档案信息的页面：

```html
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <h2>{{ employee.name }}的档案</h2>
    <form method="post">
        {% csrf_token %}
        <table>
            {{ form.as_table }}
        </table>
        <button type="submit" class="btn btn-primary">保存档案</button>
    </form>
</div>
{% endblock %}
```

---

### 6. 添加路由
在 `employee/urls.py` 中定义该视图的 URL 路径：

```python
from django.urls import path
from . import views

urlpatterns = [
    # 其他路径
    path('profile/<int:employee_id>/', views.employee_profile_view, name='employee_profile'),
]
```

---

### 7. 在员工列表中添加链接
在员工列表页面（如 `employee_list.html`）中，添加一个链接跳转到档案页面：

```html
<table>
    <thead>
        <tr>
            <th>姓名</th>
            <th>性别</th>
            <th>生日</th>
            <th>操作</th>
        </tr>
    </thead>
    <tbody>
        {% for employee in employees %}
        <tr>
            <td>{{ employee.name }}</td>
            <td>{{ employee.sex }}</td>
            <td>{{ employee.birthday }}</td>
            <td>
                <a href="{% url 'employee_profile' employee.id %}" class="btn btn-info">查看档案</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

---

### 8. 样式（可选）
为档案页面添加一些样式，使其更美观，在 `static/styles.css` 中：

```css
.container {
    margin: 20px auto;
    max-width: 800px;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
    margin-bottom: 20px;
    color: #333;
}

form table {
    width: 100%;
    margin-bottom: 20px;
}

form table tr td {
    padding: 10px 5px;
}

.btn {
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    text-decoration: none;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.btn:hover {
    background-color: #0056b3;
}
```

---

### 最终效果
1. 在员工列表中，可以点击“查看档案”进入档案页面。
2. 在档案页面中，可以填写或编辑员工的能力、培训经历和工作经验。
3. 提交后，信息会保存到数据库，并更新到对应员工的档案中。

这样设计后，员工档案不仅能记录较长的文本信息，还可以随时更新，非常适合人力资源管理系统的需求。