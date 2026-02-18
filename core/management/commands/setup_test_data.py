from django.core.management.base import BaseCommand
from core.models import User
from tasks.models import Task
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populates the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')

        # Create Users
        admin_user, _ = User.objects.get_or_create(username='admin', email='admin@example.com', role='admin')
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

        manager_user, _ = User.objects.get_or_create(username='manager', email='manager@example.com', role='manager')
        manager_user.set_password('manager123')
        manager_user.save()

        staff_user, _ = User.objects.get_or_create(username='staff', email='staff@example.com', role='staff')
        staff_user.set_password('staff123')
        staff_user.save()

        # Create Tasks
        tasks = [
            {
                'title': 'Review Q1 Financials',
                'description': 'Analyze the financial reports for the first quarter.',
                'status': 'in_progress',
                'priority': 'high',
                'assigned_to': manager_user,
                'created_by': admin_user
            },
            {
                'title': 'Update Website Content',
                'description': 'Refresh the homepage banners and update the about us page.',
                'status': 'pending',
                'priority': 'medium',
                'assigned_to': staff_user,
                'created_by': manager_user
            },
            {
                'title': 'Server Maintenance',
                'description': 'Perform routine maintenance on the production servers.',
                'status': 'completed',
                'priority': 'high',
                'assigned_to': staff_user,
                'created_by': admin_user
            }
        ]

        for task_data in tasks:
            Task.objects.get_or_create(
                title=task_data['title'],
                defaults=task_data
            )

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
        self.stdout.write(self.style.SUCCESS('Users created:'))
        self.stdout.write(' - Admin: admin / admin123')
        self.stdout.write(' - Manager: manager / manager123')
        self.stdout.write(' - Staff: staff / staff123')
