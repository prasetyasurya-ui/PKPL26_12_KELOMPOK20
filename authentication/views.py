from datetime import timedelta
import uuid

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import ECommerceRegisterForm, StyledAuthenticationForm
from .models import LoginAttempt, UserProfile

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 15
ROLE_LABELS = dict(UserProfile.ROLE_CHOICES)


def _client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


def _get_attempt(username, ip_address):
    attempt, _ = LoginAttempt.objects.get_or_create(
        username=username,
        ip_address=ip_address,
    )
    return attempt


def _ensure_role_groups():
    for role_code, _ in UserProfile.ROLE_CHOICES:
        Group.objects.get_or_create(name=role_code)


@login_required
def auth_home(request):
    role_code = None
    if request.user.is_superuser or request.user.is_staff:
        role_code = 'admin'
    elif hasattr(request.user, 'profile'):
        role_code = request.user.profile.role

    role_label = ROLE_LABELS.get(role_code, 'Admin' if role_code == 'admin' else 'Belum ditentukan')
    return render(request, 'home.html', {'role_label': role_label})


def register_view(request):
    _ensure_role_groups()

    if request.method == "POST":
        form = ECommerceRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.is_superuser = False
            user.save()

            selected_role = form.cleaned_data['role']
            role_group, _ = Group.objects.get_or_create(name=selected_role)
            user.groups.add(role_group)

            UserProfile.objects.create(user=user, role=selected_role)

            login(request, user)
            request.session.cycle_key()
            request.session['session_token'] = uuid.uuid4().hex
            return redirect('auth_home')
        messages.error(request, 'Registrasi gagal. Periksa kembali data Anda.')
    else:
        form = ECommerceRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = StyledAuthenticationForm(request, data=request.POST)
        username = request.POST.get('username', '').strip().lower()
        ip_address = _client_ip(request)
        now = timezone.now()

        attempt = None
        if username:
            attempt = _get_attempt(username, ip_address)
            if attempt.locked_until and attempt.locked_until > now:
                wait_minutes = max(1, int((attempt.locked_until - now).total_seconds() // 60))
                form.add_error(None, f"Akun sementara dikunci. Coba lagi dalam {wait_minutes} menit.")
                return render(request, 'login.html', {'form': form})

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session.cycle_key()
            request.session['session_token'] = uuid.uuid4().hex

            if attempt:
                attempt.failed_attempts = 0
                attempt.locked_until = None
                attempt.save(update_fields=['failed_attempts', 'locked_until', 'last_attempt_at'])

            return redirect('auth_home')

        if attempt:
            attempt.failed_attempts += 1
            if attempt.failed_attempts >= MAX_FAILED_ATTEMPTS:
                attempt.locked_until = now + timedelta(minutes=LOCKOUT_MINUTES)
                attempt.failed_attempts = 0
            attempt.save(update_fields=['failed_attempts', 'locked_until', 'last_attempt_at'])

        messages.error(request, 'Login gagal. Username/password salah atau akun terkunci sementara.')
    else:
        form = StyledAuthenticationForm(request)
    return render(request, 'login.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')