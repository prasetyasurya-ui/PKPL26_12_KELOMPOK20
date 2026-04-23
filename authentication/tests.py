from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import UserProfile


class AuthRoleTests(TestCase):
	def test_register_assigns_selected_role_and_profile(self):
		response = self.client.post(
			reverse('register'),
			{
				'username': 'buyer01',
				'password1': 'SafePass123!',
				'password2': 'SafePass123!',
				'role': UserProfile.ROLE_BUYER,
			},
		)

		self.assertRedirects(response, reverse('auth_home'))
		user = User.objects.get(username='buyer01')
		self.assertEqual(user.profile.role, UserProfile.ROLE_BUYER)
		self.assertTrue(user.groups.filter(name=UserProfile.ROLE_BUYER).exists())

	def test_home_shows_user_role_label(self):
		user = User.objects.create_user(username='courier01', password='SafePass123!')
		UserProfile.objects.create(user=user, role=UserProfile.ROLE_COURIER)
		self.client.login(username='courier01', password='SafePass123!')

		response = self.client.get(reverse('auth_home'))

		self.assertContains(response, 'Kurir')
