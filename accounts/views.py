from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.conf import settings  # for DEFAULT_FROM_EMAIL

from .forms import RegisterForm, CustomAuthenticationForm, ChangeEmailForm, CustomPasswordChangeForm
from .tokens import make_activation_data, decode_uid

User = get_user_model()


# -------------------------
# Helper to authenticate by username/email/phone
# -------------------------
def authenticate_by_identifier(request, identifier, password):
    # Try username first
    user = authenticate(request, username=identifier, password=password)
    if user:
        return user
    # Try email
    try:
        u = User.objects.get(email__iexact=identifier)
        user = authenticate(request, username=u.username, password=password)
        if user:
            return user
    except User.DoesNotExist:
        pass
    # Try phone (only if field exists)
    if hasattr(User, 'phone_number'):
        try:
            u = User.objects.get(phone_number=identifier)
            user = authenticate(request, username=u.username, password=password)
            if user:
                return user
        except User.DoesNotExist:
            pass
    return None


# -------------------------
# Register view
# -------------------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            uid, token = make_activation_data(user)
            activation_link = request.build_absolute_uri(
                reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})
            )
            send_mail(
                'Activate your account',
                f'Hi {user.username},\n\nPlease activate your account by clicking the link below:\n{activation_link}\n\nIf you did not sign up, ignore this email.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return render(request, 'accounts/activation_sent.html', {'email': user.email})
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# -------------------------
# Activation
# -------------------------
def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('accounts:login')
    else:
        return render(request, 'accounts/activation_invalid.html')


# -------------------------
# Login
# -------------------------
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            identifier = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember_me')

            user = authenticate_by_identifier(request, identifier, password)
            if user:
                if not user.is_active:
                    messages.error(request, 'Account not activated. Check your email for activation link.')
                    return redirect('accounts:login')
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)  # expires on browser close
                else:
                    request.session.set_expiry(None)  # use global SESSION_COOKIE_AGE
                return redirect('accounts:authorized')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


# -------------------------
# Logout
# -------------------------
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')


# -------------------------
# Authorized page
# -------------------------
@login_required
def authorized_view(request):
    return render(request, 'accounts/authorized.html')


# -------------------------
# Resend activation
# -------------------------
@require_POST
def resend_activation(request):
    email = request.POST.get('email')
    try:
        user = User.objects.get(email__iexact=email)
        if user.is_active:
            messages.info(request, 'Account already active. Try logging in.')
        else:
            uid, token = make_activation_data(user)
            link = request.build_absolute_uri(reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token}))
            send_mail('Activation link', f'Activate: {link}', settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            messages.success(request, 'Activation email resent.')
    except User.DoesNotExist:
        messages.error(request, 'No account with that email')
    return redirect('accounts:login')


# -------------------------
# Remind username
# -------------------------
def remind_username(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email__iexact=email)
            send_mail('Your username', f'Your username: {user.username}', settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
            messages.success(request, 'Your username has been emailed to you.')
        except User.DoesNotExist:
            messages.error(request, 'No account with that email')
        return redirect('accounts:login')
    return render(request, 'accounts/remind_username.html')


# -------------------------
# Change email request
# -------------------------
@login_required
def change_email_request(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            password = form.cleaned_data['password']
            if not request.user.check_password(password):
                messages.error(request, 'Password incorrect')
            else:
                uid = urlsafe_base64_encode(force_bytes(request.user.pk))
                token = default_token_generator.make_token(request.user)
                confirm_link = request.build_absolute_uri(
                    reverse(
                        'accounts:confirm_change_email',
                        kwargs={'uidb64': uid, 'token': token, 'new_email': new_email}
                    )
                )
                send_mail('Confirm email change', f'Please confirm email change by clicking: {confirm_link}', settings.DEFAULT_FROM_EMAIL, [new_email], fail_silently=False)
                messages.success(request, 'Confirmation link sent to new email')
                return redirect('accounts:authorized')
    else:
        form = ChangeEmailForm()
    return render(request, 'accounts/change_email.html', {'form': form})


# -------------------------
# Confirm change email
# -------------------------
def confirm_change_email(request, uidb64, token, new_email):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.email = new_email
        user.save()
        messages.success(request, 'Email changed successfully')
        return redirect('accounts:authorized')
    messages.error(request, 'Invalid email change link')
    return redirect('accounts:authorized')


# -------------------------
# Password reset/change views
# -------------------------
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    PasswordChangeView, PasswordChangeDoneView
)


class MyPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/activation_email.txt'


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    success_url = '/accounts/password_change/done/'


class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'
