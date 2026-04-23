from django.db import models
from django.contrib.auth.models import User


class LoginAttempt(models.Model):
	username = models.CharField(max_length=150)
	ip_address = models.GenericIPAddressField()
	failed_attempts = models.PositiveSmallIntegerField(default=0)
	locked_until = models.DateTimeField(null=True, blank=True)
	last_attempt_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ('username', 'ip_address')

	def __str__(self):
		return f"{self.username}@{self.ip_address} ({self.failed_attempts})"


class UserProfile(models.Model):
	ROLE_BUYER = 'pembeli'
	ROLE_SELLER = 'penjual'
	ROLE_COURIER = 'kurir'

	ROLE_CHOICES = [
		(ROLE_BUYER, 'Pembeli'),
		(ROLE_SELLER, 'Penjual'),
		(ROLE_COURIER, 'Kurir'),
	]

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_BUYER)
	phone_number = models.CharField(max_length=20, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} ({self.get_role_display()})"
