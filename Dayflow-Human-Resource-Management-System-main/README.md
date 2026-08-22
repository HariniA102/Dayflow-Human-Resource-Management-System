# Dayflow — Human Resource Management System

A Django implementation of the Dayflow HRMS requirements: secure authentication,
role-based dashboards, employee profile management, attendance tracking,
leave/time-off management, and payroll visibility with approval workflows.

## Requirements mapped to this project

| Spec section | Feature | Implementation |
|---|---|---|
| 3.1.1 / 3.1.2 | Sign up / Sign in | `accounts` app — Employee ID, Email, Password, Role at signup; email or username login; email verification |
| 3.2.1 / 3.2.2 | Employee & Admin dashboards | `dashboard` app |
| 3.3 | Employee profile management | `employees` app — view/edit own profile, admin edits all fields |
| 3.4 | Attendance management | `attendance` app — check-in/out, daily/weekly view, admin view of all employees |
| 3.5 | Leave & time-off management | `leaves` app — apply, approve/reject with comments, syncs into attendance |
| 3.6 | Payroll/salary management | `payroll` app — read-only employee view, admin edit + payslip generation |

## Project layout

```
dayflow_hrms/
├── manage.py
├── requirements.txt
├── dayflow_hrms/        # project settings, urls, wsgi/asgi
├── accounts/             # custom User model, auth views, role decorator
├── employees/             # profiles, documents, employee directory
├── attendance/            # check-in/out, attendance records
├── leaves/                 # leave requests & approvals
├── payroll/                # salary structures & payslips
├── dashboard/              # role-based dashboards
├── templates/               # all HTML templates (Bootstrap 5)
└── static/css/dayflow.css   # custom styling
```

## Setup

1. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Apply migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create a superuser** (optional — for `/admin/`)

   ```bash
   python manage.py createsuperuser
   ```

4. **(Optional) Seed demo data** — creates one Admin/HR user and three
   Employee users with sample attendance, leave, and salary data:

   ```bash
   python manage.py seed_demo_data
   ```

   This creates:
   - Admin/HR: `hr_admin` / `DayflowAdmin@123`
   - Employees: `priya_menon`, `rahul_singh`, `neha_patel` / `Employee@123`

5. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000/` — you'll be redirected to sign in or sign up.

## Notes

- **Email verification**: the console email backend is enabled by default, so
  verification links print to the terminal running `runserver` instead of
  being sent through a real mail server. Swap `EMAIL_BACKEND` in
  `dayflow_hrms/settings.py` for SMTP settings to send real emails.
- **Roles**: choosing "Employee" or "Admin / HR Officer" at signup determines
  which dashboard and permissions the account receives. Role-gated views use
  the `admin_required` decorator in `accounts/decorators.py`.
- **File uploads**: profile pictures and documents are stored under `media/`.
  In production, serve `MEDIA_ROOT` via your web server or object storage
  rather than Django's development server.
- **Database**: SQLite is used by default for easy setup. Point `DATABASES`
  in `settings.py` at Postgres/MySQL for production use.
- **Secret key**: replace `SECRET_KEY` in `settings.py` and set `DEBUG = False`
  with a proper `ALLOWED_HOSTS` list before deploying.

## Future enhancements (from the problem statement, section 6)

- Email & push notification alerts (leave decisions, payroll generation, etc.)
- Deeper analytics & reports dashboard (salary slip PDFs, attendance reports)
