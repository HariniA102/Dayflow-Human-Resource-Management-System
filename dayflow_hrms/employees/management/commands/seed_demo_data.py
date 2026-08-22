"""Seeds the database with a demo Admin/HR user and a few employees so
reviewers can explore Dayflow HRMS without manually signing up.

Usage:
    python manage.py seed_demo_data
"""
import datetime
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from attendance.models import Attendance
from employees.models import EmployeeProfile
from leaves.models import LeaveRequest
from payroll.models import SalaryStructure

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds demo Admin/HR and Employee accounts with sample data.'

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            username='hr_admin',
            defaults={
                'email': 'hr.admin@dayflow.example.com',
                'employee_id': 'EMP-0001',
                'first_name': 'Asha',
                'last_name': 'Rao',
                'role': User.Role.ADMIN,
                'is_email_verified': True,
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            admin.set_password('DayflowAdmin@123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin user: hr_admin / DayflowAdmin@123'))
        EmployeeProfile.objects.get_or_create(user=admin, defaults={
            'department': 'Human Resources', 'designation': 'HR Manager',
            'date_of_joining': datetime.date(2022, 1, 10),
        })

        demo_employees = [
            ('priya_menon', 'Priya', 'Menon', 'EMP-1001', 'Engineering', 'Software Engineer'),
            ('rahul_singh', 'Rahul', 'Singh', 'EMP-1002', 'Sales', 'Sales Executive'),
            ('neha_patel', 'Neha', 'Patel', 'EMP-1003', 'Design', 'UI/UX Designer'),
        ]

        for username, first, last, emp_id, dept, designation in demo_employees:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@dayflow.example.com',
                    'employee_id': emp_id,
                    'first_name': first,
                    'last_name': last,
                    'role': User.Role.EMPLOYEE,
                    'is_email_verified': True,
                },
            )
            if created:
                user.set_password('Employee@123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created employee user: {username} / Employee@123'))

            profile, _ = EmployeeProfile.objects.get_or_create(user=user)
            profile.department = dept
            profile.designation = designation
            profile.date_of_joining = datetime.date(2023, random.randint(1, 12), random.randint(1, 28))
            profile.manager = admin
            profile.save()

            SalaryStructure.objects.get_or_create(
                employee=user,
                defaults={
                    'basic': 40000, 'hra': 16000, 'conveyance_allowance': 2000,
                    'other_allowances': 3000, 'provident_fund': 4800,
                    'tax_deduction': 3500, 'other_deductions': 0,
                },
            )

            today = datetime.date.today()
            for i in range(5):
                Attendance.objects.get_or_create(
                    employee=user, date=today - datetime.timedelta(days=i),
                    defaults={'status': Attendance.Status.PRESENT,
                              'check_in': datetime.time(9, random.randint(0, 30)),
                              'check_out': datetime.time(18, random.randint(0, 30))},
                )

            LeaveRequest.objects.get_or_create(
                employee=user, leave_type=LeaveRequest.LeaveType.PAID,
                start_date=today + datetime.timedelta(days=10),
                end_date=today + datetime.timedelta(days=12),
                defaults={'remarks': 'Family function', 'status': LeaveRequest.Status.PENDING},
            )

        self.stdout.write(self.style.SUCCESS('Demo data seeding complete.'))
