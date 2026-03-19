from django.db import models
import random
from django.utils import timezone
from datetime import timedelta


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Business(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    business_name = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='businesses'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_businesses',
        
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    profile_image = models.ImageField(
        upload_to='business/profile/',
        null=True,
        blank=True
    )

    contact_person_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    mobile_no = models.CharField(max_length=15)
    mobile_verified = models.BooleanField(default=False)

    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    email_id = models.EmailField(null=True, blank=True)

    address = models.TextField()
    address_link = models.URLField(null=True, blank=True)

    instagram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)

    youtube_video_iframe = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        otp = str(random.randint(100000, 999999))
        self.otp_code = otp
        self.otp_created_at = timezone.now()
        self.mobile_verified = False
        self.save()
        return otp

    def verify_otp(self, entered_otp):
        if self.otp_code == entered_otp:
            # OTP valid for 5 minutes
            if timezone.now() <= self.otp_created_at + timedelta(minutes=5):
                self.mobile_verified = True
                self.otp_code = None
                self.save()
                return True
        return False


    def __str__(self):
        return self.business_name


class BusinessGallery(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(upload_to='business/gallery/')

    def __str__(self):
        return f"Gallery - {self.business.business_name}"

class Review(models.Model):
    business = models.ForeignKey("Business", on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=100)
    rating = models.FloatField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)