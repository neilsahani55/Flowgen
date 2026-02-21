from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile

class UserProfileModelTest(TestCase):
    def test_user_profile_creation(self):
        """Test that UserProfile is created when User is created"""
        user = User.objects.create_user(username='testuser', password='password123')
        self.assertTrue(hasattr(user, 'userprofile'))
        self.assertEqual(user.userprofile.usage_count, 0)
        self.assertEqual(user.userprofile.subscription_type, 'free')

class ViewAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.dashboard_url = reverse('content_dashboard')
        self.pagedatamaker_url = reverse('pagedatamaker')
        self.content_power_url = reverse('content_power_logic')

    def test_home_view(self):
        """Test home page access"""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_dashboard_redirect_unauthenticated(self):
        """Test dashboard returns 403 for unauthenticated users (enforced by middleware)"""
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_dashboard_access_authenticated(self):
        """Test dashboard access for authenticated users"""
        self.client.force_login(self.user)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_dashboard.html')
        # Verify the "Dashboard" title appears
        self.assertContains(response, 'Dashboard')

    def test_pagedatamaker_access_authenticated(self):
        """Test pagedatamaker access for authenticated users"""
        self.client.force_login(self.user)
        response = self.client.get(self.pagedatamaker_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pagedatamaker.html')
        # Verify it DOES NOT contain the "Dashboard" title from base_dashboard
        self.assertNotContains(response, '<h1>Dashboard</h1>')

    def test_pagedatamaker_access_unauthenticated(self):
        """Test pagedatamaker access for unauthenticated users"""
        response = self.client.get(self.pagedatamaker_url)
        self.assertEqual(response.status_code, 403)

    def test_content_power_access_authenticated(self):
        """Test content power page access for authenticated users"""
        self.client.force_login(self.user)
        response = self.client.get(self.content_power_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content_power.html')

    def test_content_power_access_unauthenticated(self):
        """Test content power page access for unauthenticated users"""
        response = self.client.get(self.content_power_url)
        self.assertEqual(response.status_code, 403)
        
    def test_login_view(self):
        """Test login functionality"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        # Login view returns JSON for AJAX or redirects.
        # If it's a standard form post (not ajax), it redirects.
        self.assertEqual(response.status_code, 302)
        
    def test_register_view_validation(self):
        """Test registration validation"""
        url = reverse('register')
        # Test short password
        response = self.client.post(url, {
            'username': 'newuser',
            'password1': 'short',
            'password2': 'short'
        })
        # Should fail and redirect to home with messages
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.home_url)

