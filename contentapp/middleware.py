# contentapp/middleware.py
from django.conf import settings
from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import PermissionDenied
import re

class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Public URLs that don't require authentication
        self.public_urls = [
            '/',  # home page
            '/login/',
            '/logout/', 
            '/register/',
            '/accounts/',
            '/admin/',
        ]
        
        # Convert to regex patterns for better matching
        self.public_patterns = [
            re.compile(r'^/$'),  # home
            re.compile(r'^/login/?$'),
            re.compile(r'^/logout/?$'), 
            re.compile(r'^/register/?$'),
            re.compile(r'^/accounts/'),
            re.compile(r'^/admin/'),
        ]

    def __call__(self, request):
        # First, check authentication for all requests
        requires_auth = True
        
        for pattern in self.public_patterns:
            if pattern.match(request.path):
                requires_auth = False
                break
        
        # If authentication required and user is not authenticated
        if requires_auth and not request.user.is_authenticated:
            return render(request, '403.html', status=403)
        
        # Then proceed with normal request processing
        try:
            response = self.get_response(request)
            
            # List of paths that should not be intercepted by custom error handling
            excluded_paths = [
                '/admin/',
                '/login/',
                '/logout/', 
                '/register/',
                '/accounts/',
            ]
            
            # Check if current path should be excluded
            should_exclude = any(request.path.startswith(path) for path in excluded_paths)
            
            # Handle 404 responses - REMOVED DEBUG CHECK
            if (response.status_code == 404 and 
                not should_exclude and
                not response.has_header('Location')):  # Don't interfere with redirects
                
                return render(request, '404.html', status=404)
            
            # Handle 403 responses - REMOVED DEBUG CHECK
            if (response.status_code == 403 and 
                not should_exclude and
                not response.has_header('Location')):
                
                return render(request, '403.html', status=403)
            
            return response
            
        except Http404 as e:
            # Handle 404 exceptions - REMOVED DEBUG CHECK
            if not request.path.startswith(('/admin/', '/login/', '/logout/', '/register/', '/accounts/')):
                return render(request, '404.html', status=404)
            raise e
            
        except PermissionDenied as e:
            # Handle 403 exceptions - REMOVED DEBUG CHECK
            if not request.path.startswith(('/admin/', '/login/', '/logout/', '/register/', '/accounts/')):
                return render(request, '403.html', status=403)
            raise e