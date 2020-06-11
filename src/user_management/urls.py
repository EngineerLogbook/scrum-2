from django.urls import path, include
from django.contrib.auth import views as auth_views
from user_management import views as user_views
urlpatterns = [
    # Custom
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('contact/', user_views.contact, name='contact'),    

    # In Built
    path('login/', auth_views.LoginView.as_view(template_name='user_management/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user_management/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user_management/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user_management/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user_management/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user_management/password_reset_complete.html'), name='password_reset_complete'),


    # For ungregisterd users

    path('', user_views.landing_page_view, name='landing-page')
]
