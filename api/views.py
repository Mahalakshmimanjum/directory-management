from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import random
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
from .models import User, Category, Business, BusinessGallery, Review
from .serializers import (
    UserSerializer,
    LoginSerializer,
    CategorySerializer,
    BusinessSerializer,
    BusinessGallerySerializer,
    ReviewSerializer
)



# ---------------- USER CRUD ----------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ---------------- LOGIN API ----------------
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = User.objects.filter(
                email=email,
                password=password
            ).first()

            if user:
                return Response(
                    {
                        "message": "Login successful",
                        "user_id": user.id,
                        "name": user.name,
                        "email": user.email
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- CATEGORY CRUD ----------------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# ---------------- BUSINESS CRUD ----------------
class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    # 🔥 FILTER BY USER
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')

        if user_id:
            return Business.objects.filter(created_by=user_id)

        return Business.objects.all()

    # 🔹 CREATE METHOD (your code + small improvement)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 🔥 Automatically assign logged-in user (optional)
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("Serializer Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- BUSINESS GALLERY CRUD ----------------
class BusinessGalleryViewSet(viewsets.ModelViewSet):
    queryset = BusinessGallery.objects.all()
    serializer_class = BusinessGallerySerializer


    # ✅ Approve Business
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        business = self.get_object()
        business.status = "approved"
        business.save()
        return Response({"message": "Business Approved Successfully"})

    # ❌ Reject Business
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        business = self.get_object()
        business.status = "rejected"
        business.save()
        return Response({"message": "Business Rejected Successfully"})

# ---------------- SEND OTP API ----------------
class SendOTPView(APIView):
    def post(self, request, business_id):
        business = get_object_or_404(Business, id=business_id)

        otp = str(random.randint(100000, 999999))
        business.otp_code = otp
        business.otp_created_at = timezone.now()
        business.mobile_verified = False
        business.save()

        print(f"OTP for {business.mobile_no}: {otp}")

        return Response({"message": "OTP sent successfully"})
        

# ---------------- VERIFY OTP API ----------------
class VerifyOTPView(APIView):
    def post(self, request, business_id):
        business = get_object_or_404(Business, id=business_id)
        entered_otp = request.data.get("otp")

        if not entered_otp:
            return Response({"error": "OTP is required"}, status=400)

        if business.otp_code == entered_otp:
            if timezone.now() <= business.otp_created_at + timedelta(minutes=5):
                business.mobile_verified = True
                business.otp_code = None
                business.save()
                return Response({"message": "Mobile verified successfully"})

        return Response({"error": "Invalid or expired OTP"}, status=400)
        
# ---------------- Review ----------------

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

