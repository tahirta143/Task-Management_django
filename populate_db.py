import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
django.setup()

from django.contrib.auth import get_user_model
from tasks.models import Task
from django.utils import timezone

User = get_user_model()

# Create users
admin_user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com', 'role': 'admin'})
admin_user.set_password('admin123')
admin_user.save()

manager_user, _ = User.objects.get_or_create(username='manager', defaults={'email': 'manager@example.com', 'role': 'manager'})
manager_user.set_password('manager123')
manager_user.save()

staff_user, _ = User.objects.get_or_create(username='staff', defaults={'email': 'staff@example.com', 'role': 'staff'})
staff_user.set_password('staff123')
staff_user.save()

print("Users created/updated: admin, manager, staff")

# Create tasks
statuses = ['pending', 'in_progress', 'completed']
priorities = ['low', 'medium', 'high']

for i in range(10):
    Task.objects.create(
        title=f'Task {i+1}',
        description=f'Description for task {i+1}',
        status=random.choice(statuses),
        priority=random.choice(priorities),
        assigned_to=staff_user,
        created_by=manager_user
    )

print("Sample tasks created.")
