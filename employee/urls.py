from django.urls import path
from .views import LoginView, RegisterView, UserView

urlpatterns = [
    path('register', RegisterView.as_view(), name='employee_register'),
    path('login', LoginView.as_view(), name='employee_login'),
    path('profile', UserView.as_view(), name='employee_profile')
]