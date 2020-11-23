from django.urls import path

from .views import UserLoginView, RegisterUserView, index 

urlpatterns = [
    path('', index, name = 'home'),
    path( 'auth/register/', RegisterUserView.as_view(), name = 'auth-register' ),
    path('auth/login/', UserLoginView.as_view() , name = 'auth-login')
]