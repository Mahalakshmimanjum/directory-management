from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    LoginView,
    CategoryViewSet,
    BusinessViewSet,
    BusinessGalleryViewSet,
    SendOTPView,
    VerifyOTPView,
    ReviewViewSet

)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'business', BusinessViewSet)
router.register(r'business-gallery', BusinessGalleryViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('send-otp/<int:business_id>/', SendOTPView.as_view()),
    path('verify-otp/<int:business_id>/', VerifyOTPView.as_view()),
]
