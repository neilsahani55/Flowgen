from django.urls import path
from . import views

urlpatterns = [
    # Authentication & User Management URLs
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # User registration
    path('login/', views.login_view, name='login'),  # User login
    path('logout/', views.logout_view, name='logout'),  # User logout
    path('profile/', views.profile_view, name='profile'),  # User profile management
    
    # Content Dashboard & Main Features
    path('content_dashboard/', views.content_dashboard, name='content_dashboard'),  # Main content dashboard
    path('comparison/', views.comparison_view, name='comparison'),  # Content comparison feature
    
    # Content Power - Main AI Content Generation
    path('content_power/', views.content_power_logic, name='content_power_logic'),  # Main content power logic
    path('content_power_api/', views.content_power_api, name='content_power_api'),  # Content power API endpoint
    path('content_power_status/', views.content_power_status, name='content_power_status'),  # Content power status check
    
    # Blog Generator Endpoints
    path('content_power/blog/', views.content_power_blog, name='content_power_blog'),  # Blog content generation
    path('content_blog_api/', views.content_blog_api, name='content_blog_api'),  # Blog content API
    path('content_blog_status/', views.content_blog_status, name='content_blog_status'),  # Blog generation status
    
    # Landing Page Generator
    path('content_power/landing_page/', views.landing_page, name='landing_page'),  # Landing page content generation
    
    # Integration & Webhook Endpoints
    path('n8n_webhook/', views.n8n_webhook, name='n8n_webhook'),  # n8n workflow integration webhook
    path('page_analysis/', views.page_analysis, name='page_analysis'), 
    path('pagedatamaker/', views.pagedatamaker, name='pagedatamaker'),
    
    # Content Display & Management
    path('blog/', views.blog, name='blog'),  # Blog content display
    
    # Reports & Analytics
    path('customer-rates/', views.CustomerRatesReport.as_view(), name='customer_rates'),  # Customer rates reporting
    
    path('webpage-updater/', views.webpage_updater, name='webpage_updater'),
    
]

# Custom Error Handlers
handler403 = 'contentapp.views.custom_403_view'
handler404 = 'contentapp.views.custom_404_view'
