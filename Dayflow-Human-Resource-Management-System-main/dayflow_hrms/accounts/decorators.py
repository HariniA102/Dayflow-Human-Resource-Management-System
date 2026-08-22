from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def admin_required(view_func):
    """Restrict a view to Admin / HR Officer users only."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_admin_role:
            messages.error(request, 'You do not have permission to access that page.')
            return redirect('dashboard:redirect')
        return view_func(request, *args, **kwargs)

    return _wrapped
