from django.urls import path
from .views import UserViewSet
from .serializers import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('user/register', UserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('user/<uuid:pk>', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update'
    }), name='user-detail'),
    path('auth/token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]