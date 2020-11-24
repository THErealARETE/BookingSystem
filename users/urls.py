from django.urls import path

from .views import UserLoginView, RegisterUserView, index , ImageUploadViewSet

# from .views import RegisterUserView, index 

urlpatterns = [
    path('', index, name = 'home'),
    path( 'auth/register/', RegisterUserView.as_view(), name = 'auth-register' ),
    path('auth/login/', UserLoginView.as_view() , name = 'auth-login'),
     path('user/upload/', ImageUploadViewSet.as_view(), name="file-upload"),
    path('user/upload/<int:pk>/', ImageUploadViewSet.as_view(), name="file-upload-detail")
]