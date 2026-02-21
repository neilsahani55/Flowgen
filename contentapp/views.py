from calendar import monthrange
from datetime import date, datetime, timedelta
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.utils import timezone


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.utils import timezone

def home(request):
    """Home page view - serves base.html"""
    # If user is already authenticated, redirect to content_dashboard
    if request.user.is_authenticated:
        return redirect('content_dashboard')
    return render(request, 'base.html')

from django.http import JsonResponse
import json

def register(request):
    """Handle user registration with AJAX support"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        errors = []
        field_errors = {}
        
        # Validation
        if not username:
            field_errors['username'] = 'Username is required.'
        elif len(username) < 3:
            field_errors['username'] = 'Username must be at least 3 characters.'
        elif User.objects.filter(username=username).exists():
            field_errors['username'] = 'Username already exists.'
        
        if not password1:
            field_errors['password1'] = 'Password is required.'
        else:
            if len(password1) < 8:
                field_errors['password1'] = 'Password must be at least 8 characters.'
            if not any(char.isdigit() for char in password1):
                field_errors['password1'] = 'Password must contain at least one number.'
            if not any(char.isupper() for char in password1):
                field_errors['password1'] = 'Password must contain at least one uppercase letter.'
            if not any(char.islower() for char in password1):
                field_errors['password1'] = 'Password must contain at least one lowercase letter.'
            if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in password1):
                field_errors['password1'] = 'Password must contain at least one special character.'
        
        if password1 != password2:
            field_errors['password2'] = 'Passwords do not match.'
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if field_errors:
                # Convert field errors to general errors for the alert
                general_errors = list(field_errors.values())
                return JsonResponse({
                    'success': False,
                    'errors': general_errors,
                    'field_errors': field_errors
                })
            else:
                try:
                    # Create user
                    user = User.objects.create_user(username=username, password=password1)
                    user.save()
                    
                    # Auto login after registration
                    user = authenticate(username=username, password=password1)
                    if user is not None:
                        login(request, user)
                        return JsonResponse({
                            'success': True,
                            'message': 'Registration successful! Welcome to our platform.',
                            'redirect_url': '/content_dashboard/'
                        })
                    else:
                        return JsonResponse({
                            'success': True,
                            'message': 'Registration successful! Please login.',
                            'redirect_url': '/'
                        })
                        
                except Exception as e:
                    return JsonResponse({
                        'success': False,
                        'errors': [f'An error occurred during registration. Please try again. Error: {str(e)}']
                    })
        
        # For non-AJAX requests (fallback)
        if field_errors:
            for error in list(field_errors.values()):
                messages.error(request, error)
            return redirect('home')
        else:
            try:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                
                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Registration successful! Welcome to our platform.')
                    return redirect('content_dashboard')
                else:
                    messages.success(request, 'Registration successful! Please login.')
                    return redirect('home')
                    
            except Exception as e:
                messages.error(request, f'An error occurred during registration. Please try again. Error: {str(e)}')
                return redirect('home')
    
    # If GET request, redirect to home
    return redirect('home')
    
    
def login_view(request):
    """Handle user login with AJAX support"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        errors = []
        field_errors = {}
        
        # Validation
        if not username:
            field_errors['username'] = 'Username is required.'
        
        if not password:
            field_errors['password'] = 'Password is required.'
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if field_errors:
                # Convert field errors to general errors for the alert
                general_errors = list(field_errors.values())
                return JsonResponse({
                    'success': False,
                    'errors': general_errors,
                    'field_errors': field_errors
                })
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Safely update last login in profile
                try:
                    profile = user.userprofile
                    profile.last_login_date = timezone.now()
                    profile.save()
                except UserProfile.DoesNotExist:
                    # Create profile if it doesn't exist
                    UserProfile.objects.create(user=user, last_login_date=timezone.now())
                
                return JsonResponse({
                    'success': True,
                    'message': f'Welcome back, {username}!',
                    'redirect_url': '/content_dashboard/'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': ['Invalid username or password.'],
                    'field_errors': {
                        'username': 'Invalid credentials',
                        'password': 'Invalid credentials'
                    }
                })
        
        # For non-AJAX requests (fallback)
        if field_errors:
            for error in list(field_errors.values()):
                messages.error(request, error)
            return redirect('home')
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Safely update last login in profile
                try:
                    profile = user.userprofile
                    profile.last_login_date = timezone.now()
                    profile.save()
                except UserProfile.DoesNotExist:
                    UserProfile.objects.create(user=user, last_login_date=timezone.now())
                
                messages.success(request, f'Welcome back, {username}!')
                return redirect('content_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('home')
    
    # If GET request, redirect to home
    return redirect('home')

def logout_view(request):
    """Handle user logout"""
    logout(request)
    return redirect('home')

def content_dashboard(request):
    """
    Only renders the base HTML dashboard.
    All functionality (forms, API calls) handled in HTML via separate URLs or AJAX.
    """
    if not request.user.is_authenticated:
        #messages.error(request, 'Please login to access the dashboard.')
        return redirect('403.html')
    
    # Safely get user profile
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)
    
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'base_dashboard.html', context)

def profile_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to view your profile.')
        return redirect('home')
    
    # Safely get user profile
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)
    
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)

import json
import uuid
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
import logging

# Configure logger
logger = logging.getLogger(__name__)


# Main view to display the form and handle form submission
def content_power_logic(request):
    if request.method == 'POST':
        try:
            # Get form data with validation
            company_name = request.POST.get('company_name', '').strip()
            company_details = request.POST.get('company_details', '').strip()
            competitor_url = request.POST.get('competitor_url', '').strip()
            competitor_content = request.POST.get('competitor_content', '').strip()
            template = request.POST.get('template', '').strip()
            template_content = request.POST.get('template_content', '').strip()
            
            # Validate required fields
            if not all([company_name, company_details, competitor_url, template]):
                return JsonResponse({
                    'success': False,
                    'message': 'All required fields must be filled'
                }, status=400)
            
            # Generate a unique session ID for this request
            session_id = str(uuid.uuid4())
            
            # Store session ID in the session
            request.session['content_power_session_id'] = session_id
            
            # Initialize cache entry for this session
            cache.set(f'content_power_{session_id}', {
                'status': 'processing',
                'content': None,
                'timestamp': None
            }, timeout=3600)  # Cache for 1 hour
            
            # Prepare payload for n8n webhook
            payload = {
                'company_name': company_name,
                'company_details': company_details,
                'competitor_url': competitor_url,
                'competitor_content': competitor_content,
                'template': template,
                'template_content': template_content,
                'session_id': session_id
            }
            
            # Log the request
            logger.info(f"Starting workflow for session: {session_id}")
            logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
            
            # Send POST request to n8n webhook
            n8n_webhook_url = 'https://mcmflow.app.n8n.cloud/webhook/Content_Power'
            response = requests.post(
                n8n_webhook_url, 
                json=payload, 
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                logger.info(f"Workflow started successfully for session: {session_id}")
                return JsonResponse({
                    'success': True,
                    'session_id': session_id,
                    'message': 'Workflow started successfully'
                })
            else:
                logger.error(f"Workflow start failed with status {response.status_code}: {response.text}")
                return JsonResponse({
                    'success': False,
                    'message': f'Error starting workflow: HTTP {response.status_code}'
                }, status=500)
                
        except requests.exceptions.Timeout:
            logger.error("Request to n8n webhook timed out")
            return JsonResponse({
                'success': False,
                'message': 'Request timed out. Please try again.'
            }, status=504)
            
        except requests.exceptions.ConnectionError:
            logger.error("Connection error to n8n webhook")
            return JsonResponse({
                'success': False,
                'message': 'Unable to connect to the workflow service. Please check your connection.'
            }, status=503)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Error connecting to workflow service: {str(e)}'
            }, status=500)
            
        except Exception as e:
            logger.error(f"Unexpected error in content_power_logic: {str(e)}", exc_info=True)
            return JsonResponse({
                'success': False,
                'message': 'An unexpected error occurred. Please try again.'
            }, status=500)
    
    # GET request - render the form
    return render(request, 'content_power.html')


# Endpoint to receive generated content from n8n
@csrf_exempt
@require_http_methods(["POST"])
def content_power_api(request):
    try:
        # Parse request body
        raw_body = request.body.decode('utf-8')
        logger.info(f"Received webhook callback. Body length: {len(raw_body)}")
        logger.debug(f"Raw body: {raw_body[:500]}...")  # Log first 500 chars
        
        # Parse JSON data from n8n
        data = json.loads(raw_body)
        
        # Extract session_id - try multiple possible keys
        session_id = (
            data.get('session_id') or 
            data.get('sessionId') or 
            data.get('session_ID') or
            data.get('Session_ID')
        )
        
        if not session_id:
            logger.error(f"No session_id found. Available keys: {list(data.keys()) if isinstance(data, dict) else 'not a dict'}")
            return JsonResponse({
                'success': False,
                'message': 'Missing session_id in webhook payload',
                'received_keys': list(data.keys()) if isinstance(data, dict) else 'not a dict'
            }, status=400)
        
        # Extract content with multiple fallback methods
        generated_content = extract_content(data)
        
        logger.info(f"Session: {session_id} - Content extracted successfully")
        logger.debug(f"Content type: {type(generated_content).__name__}")
        
        # Validate content
        if generated_content is None or (isinstance(generated_content, str) and not generated_content.strip()):
            logger.warning(f"Session: {session_id} - Content is empty or None")
        
        # Store the generated content in cache
        from datetime import datetime
        cache_data = {
            'status': 'completed',
            'content': generated_content,
            'raw_response': data,
            'timestamp': datetime.now().isoformat()
        }
        
        # Set cache with extended timeout
        cache.set(f'content_power_{session_id}', cache_data, timeout=7200)  # 2 hours
        logger.info(f"Successfully stored data in cache for session: {session_id}")
        
        return JsonResponse({
            'success': True,
            'message': 'Content received and stored successfully',
            'session_id': session_id
        })
    
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'Invalid JSON format: {str(e)}',
            'raw_body_preview': request.body.decode('utf-8')[:200]
        }, status=400)
        
    except Exception as e:
        logger.error(f"Unexpected error in content_power_api: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': f'Server error: {str(e)}'
        }, status=500)


def extract_content(data):
    """
    Extract content from various possible data structures sent by n8n
    """
    # Method 1: Direct content key
    if 'content' in data:
        return data['content']
    
    # Method 2: Output key (common in n8n)
    if 'output' in data:
        return data['output']
    
    # Method 3: Result key
    if 'result' in data:
        return data['result']
    
    # Method 4: Data key
    if 'data' in data:
        return data['data']
    
    # Method 5: Array with content
    if isinstance(data, list) and len(data) > 0:
        first_item = data[0]
        if isinstance(first_item, dict):
            return extract_content(first_item)
        return data
    
    # Method 6: Body key (some webhooks wrap content)
    if 'body' in data:
        return extract_content(data['body'])
    
    # Method 7: The entire payload is the content (excluding session identifiers)
    if isinstance(data, dict):
        content_copy = data.copy()
        # Remove known metadata keys
        for key in ['session_id', 'sessionId', 'session_ID', 'Session_ID', 'timestamp', 'metadata']:
            content_copy.pop(key, None)
        
        # If there's only one key left, return its value
        if len(content_copy) == 1:
            return list(content_copy.values())[0]
        
        # If there's content left, return it
        if content_copy:
            return content_copy
    
    # Method 8: Return as-is if it's a string
    if isinstance(data, str):
        return data
    
    # Last resort: return the entire data
    return data


# Polling endpoint for frontend to check content status
@require_http_methods(["GET"])
def content_power_status(request):
    session_id = request.GET.get('session_id')
    
    if not session_id:
        return JsonResponse({
            'success': False,
            'message': 'Missing session_id parameter'
        }, status=400)
    
    # Retrieve content from cache
    cached_data = cache.get(f'content_power_{session_id}')
    
    if cached_data is None:
        logger.warning(f"Session not found or expired: {session_id}")
        return JsonResponse({
            'success': False,
            'status': 'not_found',
            'message': 'Session not found or expired'
        })
    
    # Log status check
    status = cached_data.get('status', 'unknown')
    logger.debug(f"Status check for session {session_id}: {status}")
    
    # Prepare response
    response_data = {
        'success': True,
        'status': status,
        'content': cached_data.get('content'),
        'timestamp': cached_data.get('timestamp')
    }
    
    # Add debug info only if content is present
    if status == 'completed':
        content = cached_data.get('content')
        response_data['debug_info'] = {
            'content_type': type(content).__name__,
            'content_length': len(str(content)) if content else 0,
            'has_content': content is not None and (
                (isinstance(content, str) and content.strip()) or
                (not isinstance(content, str))
            )
        }
    
    return JsonResponse(response_data)


# Optional: Add endpoint to clear session cache
@require_http_methods(["POST"])
def content_power_clear_session(request):
    """Clear a specific session from cache"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        
        if not session_id:
            return JsonResponse({
                'success': False,
                'message': 'Missing session_id'
            }, status=400)
        
        cache.delete(f'content_power_{session_id}')
        logger.info(f"Cleared cache for session: {session_id}")
        
        return JsonResponse({
            'success': True,
            'message': 'Session cleared successfully'
        })
        
    except Exception as e:
        logger.error(f"Error clearing session: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
        
###Content_power_blog

import json
import uuid
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.cache import cache

# ============================================================================
# BLOG GENERATOR VIEWS (Separate from homepage generator)
# ============================================================================

# Main view to display the blog form
def content_power_blog(request):
    """
    Serves the blog generation UI at /content_power/blog
    """
    # Optionally generate server-side job_id
    job_id = str(uuid.uuid4())
    
    return render(request, 'content_power_blog.html', {
        'job_id': job_id
    })


# Endpoint to receive generated blog content from n8n
@csrf_exempt
@require_http_methods(["POST"])
def content_blog_api(request):
    """
    Callback endpoint at /content_blog_api/
    Receives completed blog content from n8n
    """
    try:
        import logging
        logger = logging.getLogger(__name__)
        
        # Handle both JSON and form-data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = dict(request.POST.items())
        
        logger.info(f"Blog API received data: {data}")
        
        # Extract required fields
        job_id = data.get('job_id') or data.get('jobId')
        html_content = data.get('html')
        
        if not job_id:
            logger.error("No job_id found in blog callback")
            return JsonResponse({
                'ok': False,
                'error': 'Missing job_id'
            }, status=400)
        
        if not html_content:
            logger.warning(f"No HTML content for job_id: {job_id}")
            # Store error state
            cache.set(f'blog_job_{job_id}', {
                'status': 'completed',
                'error': 'No HTML content received from workflow'
            }, timeout=1800)  # 30 minutes
            
            return JsonResponse({
                'ok': True,
                'message': 'Job stored with error'
            })
        
        # Extract optional fields
        meta_title = data.get('meta_title') or data.get('metaTitle')
        meta_description = data.get('meta_description') or data.get('metaDescription')
        image1 = data.get('image1')
        image2 = data.get('image2')
        image3 = data.get('image3')
        
        # Store the completed blog data
        blog_data = {
            'status': 'completed',
            'html': html_content,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'image1': image1,
            'image2': image2,
            'image3': image3,
            'raw_data': data
        }
        
        cache.set(f'blog_job_{job_id}', blog_data, timeout=1800)  # 30 minutes
        logger.info(f"Successfully stored blog data for job_id: {job_id}")
        
        return JsonResponse({
            'ok': True,
            'message': 'Blog content received successfully'
        })
    
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in blog API: {str(e)}")
        return JsonResponse({
            'ok': False,
            'error': f'Invalid JSON: {str(e)}'
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in blog API: {str(e)}", exc_info=True)
        return JsonResponse({
            'ok': False,
            'error': str(e)
        }, status=500)


# Polling endpoint for frontend to check blog status
@require_http_methods(["GET"])
def content_blog_status(request):
    """
    Polling endpoint at /content_blog_status/?job_id=...
    Frontend polls this to check if blog is ready
    """
    job_id = request.GET.get('job_id')
    
    if not job_id:
        return JsonResponse({
            'success': False,
            'error': 'Missing job_id parameter'
        }, status=400)
    
    # Retrieve blog data from cache
    blog_data = cache.get(f'blog_job_{job_id}')
    
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Blog status check for job_id {job_id}: {blog_data}")
    
    if blog_data is None:
        # Job not found or not completed yet
        return JsonResponse({
            'success': True,
            'status': 'pending'
        })
    
    # Check if there's an error
    if blog_data.get('error'):
        return JsonResponse({
            'success': True,
            'status': 'completed',
            'error': blog_data['error']
        })
    
    # Return the completed blog data
    return JsonResponse({
        'success': True,
        'status': 'completed',
        'data': {
            'html': blog_data.get('html'),
            'meta_title': blog_data.get('meta_title'),
            'meta_description': blog_data.get('meta_description'),
            'image1': blog_data.get('image1'),
            'image2': blog_data.get('image2'),
            'image3': blog_data.get('image3')
        }
    })
    
    
    
def landing_page(request):
    """
    Serves the blog generation UI at /content_power/page
    """
     
    return render(request, 'content_power_page.html', {
      
         
    })
    
    
def comparison_view(request):
    return render(request, "comparison.html")    

#rahul mauriya
def n8n_webhook(request):
    return render(request, 'n8n_result.html')
    




#rahul mauriya
def page_analysis(request):
    return render(request, 'pageanalysis.html')
    
    
def blog(request):
  
    return render(request, 'blog.html')
    
    
    
##################################customer_report##################################################

import requests
import csv
from io import StringIO
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from collections import defaultdict

class CustomerRatesReport(View):
    
    # Cache to store merged carrier data
    _carrier_cache = {}
    _cache_timeout = 3600  # 1 hour cache
    
    PROVIDER_TOKENS = {
        'acepeak': '',
        'teloz': '',
        'letsdial': '',
        'twiching': '',
        'twichinggeneraltrading': '',
        'softtop': '',
        'rozper': '',
        'rozpar': '',
        'meratalk': '',
        'techopensystem': '',
        'techopensystems': '',
        'ajoxi': '',
        'mcm': '',
    }
    
    # Provider API domain mapping
    PROVIDER_API_DOMAIN = {
        'acepeak': 'acepeak',
        'teloz': 'teloz',
        'letsdial': 'letsdial',
        'twiching': 'twiching',
        'twichinggeneraltrading': 'twiching',
        'softtop': 'softtop',
        'rozper': 'rozper',
        'rozpar': 'rozper',
        'meratalk': 'meratalk',
        'techopensystem': 'techopensystems',
        'techopensystems': 'techopensystems',
        'ajoxi': 'ajoxi',
        'mcm': 'mcm',
    }
    
    # Provider name mapping
    PROVIDER_MAPPING = {
        'twitching': 'twiching',
        'techopensystem': 'techopensystems',
        'rozpar': 'rozper',
    }
    
    # Field name mappings for CSV columns
    RATE_FIELD_MAPPINGS = {
        'interrate': ['interrate', 'inter_rate', 'inter', 'interprice', 'rate', 'inter rate'],
        'intrarate': ['intrarate', 'intra_rate', 'intra', 'intraprice', 'intra rate'],
        'code': ['code', 'dial_code', 'dialcode', 'prefix', 'destination_code']
    }
    
    def get(self, request):
        """Render the main page with carrier list"""
        action = request.GET.get('action')
        
        if action == 'get_all_carriers':
            carriers = self.fetch_all_carriers()
            return JsonResponse({'carriers': carriers}, safe=False)
        
        elif action == 'clear_cache':
            # Clear the cache
            self._carrier_cache.clear()
            print("[CACHE] Cache cleared")
            return JsonResponse({'status': 'success', 'message': 'Cache cleared'})
        
        return render(request, 'customer_report.html')
    
    def post(self, request):
        """Handle AJAX request to fetch merged carrier rates for comparison"""
        carrier_data = request.POST.get('carrier_data', '[]')
        page = int(request.POST.get('page', 1))
        page_size = int(request.POST.get('page_size', 50))
        
        try:
            import json
            carriers = json.loads(carrier_data)
            
            if not carriers:
                return JsonResponse({'error': 'No carriers selected'}, status=400)
            
            comparison_data = self.fetch_merged_carrier_rates(carriers, page, page_size)
            return JsonResponse(comparison_data, safe=False)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    
    def fetch_all_carriers(self):
        """Fetch all carriers from the contact API"""
        print("[FETCH_CARRIERS] Starting...")
        try:
            url = 'http://70.36.107.109:1920/peeredgelabs_contact_api/'
            response = requests.get(url, auth=('customwpform', 'customwpform'), timeout=30, verify=False)
            response.raise_for_status()
            data = response.json()
            
            carriers = data.get('carriers', data.get('data', [])) if isinstance(data, dict) else data
            if not isinstance(carriers, list):
                return []
            
            valid_carriers = []
            for carrier in carriers:
                provider = carrier.get('provider', '').lower().strip()
                provider = self.PROVIDER_MAPPING.get(provider, provider)
                
                if provider in self.PROVIDER_TOKENS:
                    carrier['provider'] = provider
                    valid_carriers.append(carrier)
            
            carriers_sorted = sorted(valid_carriers, key=lambda x: x.get('carrier_name', ''))
            print(f"[FETCH_CARRIERS] Found {len(carriers_sorted)} valid carriers")
            return carriers_sorted
        except Exception as e:
            print(f"[FETCH_CARRIERS] ERROR: {e}")
            return []
    
    def fetch_merged_carrier_rates(self, carriers, page=1, page_size=50):
        """Fetch and merge all trunk rates for each carrier with caching"""
        print(f"\n[COMPARISON] Page {page}, Size {page_size}")
        print(f"[COMPARISON] Processing {len(carriers)} carriers")
        
        result = {
            'carriers': [],
            'comparison_data': [],
            'pagination': {'page': page, 'page_size': page_size, 'total_codes': 0, 'total_pages': 0}
        }
        
        # Fetch merged data for each carrier (with caching)
        carrier_merged_data = []
        for idx, carrier in enumerate(carriers):
            carrier_id = carrier.get('carrier_id')
            provider = carrier.get('provider')
            carrier_name = carrier.get('carrier_name', 'Unknown')
            
            # Create cache key
            cache_key = f"{carrier_id}_{provider}"
            
            # Check cache
            import time
            current_time = time.time()
            cached_data = self._carrier_cache.get(cache_key)
            
            if cached_data and (current_time - cached_data['timestamp']) < self._cache_timeout:
                print(f"[CARRIER_{idx+1}] {carrier_name} (CACHED)")
                merged_rates = cached_data['rates']
            else:
                print(f"[CARRIER_{idx+1}] {carrier_name} (ID: {carrier_id}, Provider: {provider})")
                merged_rates = self.get_merged_carrier_rates(carrier_id, provider)
                
                # Store in cache
                if merged_rates:
                    self._carrier_cache[cache_key] = {
                        'rates': merged_rates,
                        'timestamp': current_time
                    }
            
            if merged_rates:
                carrier_merged_data.append({
                    'carrier_id': carrier_id,
                    'carrier_name': carrier_name,
                    'provider': provider,
                    'rates': merged_rates
                })
                result['carriers'].append({
                    'name': carrier_name,
                    'provider': provider,
                    'total_codes': len(merged_rates)
                })
                print(f"[CARRIER_{idx+1}] Using {len(merged_rates)} unique codes")
            else:
                print(f"[CARRIER_{idx+1}] No data found")
        
        if not carrier_merged_data:
            print("[COMPARISON] No carrier data collected")
            return result
        
        # Get all unique codes
        all_codes = set()
        for carrier_data in carrier_merged_data:
            all_codes.update(carrier_data['rates'].keys())
        
        sorted_codes = sorted(list(all_codes))
        total_codes = len(sorted_codes)
        print(f"[COMPARISON] Total unique codes: {total_codes}")
        
        # Pagination
        total_pages = (total_codes + page_size - 1) // page_size if total_codes > 0 else 1
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_codes = sorted_codes[start_idx:end_idx]
        
        # Build comparison data
        for code in page_codes:
            comparison_row = {'code': code, 'rates': []}
            
            for carrier_data in carrier_merged_data:
                rate_data = carrier_data['rates'].get(code, {'interrate': '-', 'intrarate': '-'})
                comparison_row['rates'].append(rate_data)
            
            result['comparison_data'].append(comparison_row)
        
        result['pagination'] = {
            'page': page,
            'page_size': page_size,
            'total_codes': total_codes,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
        
        print(f"[COMPARISON] Built {len(result['comparison_data'])} rows for page {page}")
        return result
    
    def get_merged_carrier_rates(self, carrier_id, provider):
        """Get all trunks for a carrier and merge their rates"""
        provider_lower = provider.lower().strip()
        token = self.PROVIDER_TOKENS.get(provider_lower)
        api_domain = self.PROVIDER_API_DOMAIN.get(provider_lower)
        
        if not token or not api_domain:
            print(f"[MERGE] Missing token or domain for {provider}")
            return {}
        
        try:
            url = f'https://api-{api_domain}.peeredge.com/api/v2/rate_sheets?carrier_id={carrier_id}'
            headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            rate_sheets = response.json()
            
            if not rate_sheets:
                print(f"[MERGE] No rate sheets found")
                return {}
            
            print(f"[MERGE] Found {len(rate_sheets)} rate sheets")
            
            # Merge all rates from all trunks
            merged_rates = {}
            
            for sheet_idx, sheet in enumerate(rate_sheets):
                upload_url = sheet.get('upload_url', '')
                if not upload_url:
                    continue
                
                csv_data = self.fetch_csv_data(upload_url, sheet_idx + 1)
                
                for row in csv_data:
                    code = self.get_field_value(row, 'code')
                    if not code:
                        continue
                    
                    interrate = self.get_field_value(row, 'interrate')
                    intrarate = self.get_field_value(row, 'intrarate')
                    
                    # If intrarate is missing, use interrate
                    if not intrarate and interrate:
                        intrarate = interrate
                    
                    # Convert 0 to -
                    if interrate == '0':
                        interrate = '-'
                    if intrarate == '0':
                        intrarate = '-'
                    
                    # Store or update rate (keep first non-empty value found)
                    if code not in merged_rates:
                        merged_rates[code] = {
                            'interrate': interrate if interrate else '-',
                            'intrarate': intrarate if intrarate else '-'
                        }
                    else:
                        # Update if current value is '-' and new value is not
                        if merged_rates[code]['interrate'] == '-' and interrate and interrate != '-':
                            merged_rates[code]['interrate'] = interrate
                        if merged_rates[code]['intrarate'] == '-' and intrarate and intrarate != '-':
                            merged_rates[code]['intrarate'] = intrarate
            
            print(f"[MERGE] Merged to {len(merged_rates)} unique codes")
            return merged_rates
            
        except Exception as e:
            print(f"[MERGE] ERROR: {e}")
            return {}
    
    def fetch_csv_data(self, url, sheet_num):
        """Fetch and parse CSV data"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            csv_content = response.text
            csv_reader = csv.DictReader(StringIO(csv_content))
            
            data = []
            for row in csv_reader:
                cleaned_row = {}
                for key, value in row.items():
                    if key:
                        clean_key = key.strip().lower()
                        clean_value = value.strip() if value else ''
                        cleaned_row[clean_key] = clean_value
                data.append(cleaned_row)
            
            print(f"[SHEET_{sheet_num}] Parsed {len(data)} rows")
            return data
            
        except Exception as e:
            print(f"[CSV] ERROR: {e}")
            return []
    
    def get_field_value(self, row, field_type):
        """Get field value from row using multiple possible field names"""
        possible_names = self.RATE_FIELD_MAPPINGS.get(field_type, [field_type])
        
        for field_name in possible_names:
            value = row.get(field_name, '').strip()
            if value:
                return value
        
        return ''
        
def custom_404_view(request, exception=None):
    """Custom 404 view that works in both debug and production"""
    return render(request, '404.html', status=404)

def custom_403_view(request, exception=None):
    """Custom 403 view that works in both debug and production"""
    return render(request, '403.html', status=403)

def pagedatamaker(request):
    """View for Page Data Maker"""
    return render(request, 'pagedatamaker.html')
    
    
from django.shortcuts import render

def webpage_updater(request):
    return render(request, 'pagedataupdater.html')
    
