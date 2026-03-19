from rest_framework import serializers
from .models import User, Category, Business, BusinessGallery,Review


# ---------------- USER ----------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# ---------------- LOGIN ----------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# ---------------- CATEGORY ----------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# ---------------- BUSINESS GALLERY ----------------
class BusinessGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessGallery
        fields = ['id', 'image']


# ---------------- BUSINESS ----------------
class BusinessSerializer(serializers.ModelSerializer):
    # read gallery images
    gallery_images = BusinessGallerySerializer(many=True, read_only=True)

    # write-only field for multiple image upload
    gallery_uploads = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Business
        fields = '__all__'

    def create(self, validated_data):
        gallery_files = validated_data.pop('gallery_uploads', [])
        business = Business.objects.create(**validated_data)

        for image in gallery_files:
            BusinessGallery.objects.create(
                business=business,
                image=image
            )

        return business
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"