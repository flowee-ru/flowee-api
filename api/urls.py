from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.CreateUserView.as_view(), name='create_user'),
    path('users/<str:username>/', views.RetrieveUserView.as_view(), name='retrieve_user'),
]
