from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_view, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('authorized/', views.authorized_view, name='authorized'),
    path('resend-activation/', views.resend_activation, name='resend_activation'),
    path('remind-username/', views.remind_username, name='remind_username'),
    path('change-email/', views.change_email_request, name='change_email_request'),
    path('confirm-change-email/<uidb64>/<token>/<new_email>/', views.confirm_change_email, name='confirm_change_email'),

    # password reset/change
    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', views.MyPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.MyPasswordChangeDoneView.as_view(), name='password_change_done'),
]
