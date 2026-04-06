"""
URL configuration for finance backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# API Root view
def api_root(request):
    
    return JsonResponse({
        'message': 'Welcome to Finance Dashboard API',
        'version': '1.0.0',
        'status': 'online',
        'documentation': {
            'swagger': request.build_absolute_uri('/api/docs/'),
            'redoc': request.build_absolute_uri('/api/redoc/'),
        },
        'endpoints': {
            'authentication': {
                'register': request.build_absolute_uri('/api/auth/register/'),
                'login': request.build_absolute_uri('/api/auth/login/'),
                'refresh': request.build_absolute_uri('/api/auth/refresh/'),
            },
            'users': {
                'list': request.build_absolute_uri('/api/users/'),
                'me': request.build_absolute_uri('/api/users/me/'),
            },
            'records': {
                'list': request.build_absolute_uri('/api/records/'),
                'my_records': request.build_absolute_uri('/api/records/my-records/'),
                'stats': request.build_absolute_uri('/api/records/stats/'),
            },
            'dashboard': {
                'summary': request.build_absolute_uri('/api/dashboard/summary/'),
                'category_wise': request.build_absolute_uri('/api/dashboard/category-wise/'),
                'trends': request.build_absolute_uri('/api/dashboard/trends/'),
                'recent': request.build_absolute_uri('/api/dashboard/recent/'),
                'top_expenses': request.build_absolute_uri('/api/dashboard/top-expenses/'),
            }
        },
        'demo_credentials': {
            'admin': {
                'username': 'demo_admin',
                'password': 'DemoAdmin123!',
                'note': 'Full access - Create, Update, Delete'
            },
            'analyst': {
                'username': 'demo_analyst',
                'password': 'DemoAnalyst123!',
                'note': 'View all records - Read only'
            },
            'viewer': {
                'username': 'demo_viewer',
                'password': 'DemoViewer123!',
                'note': 'View own records only'
            }
        },
        'quick_start': {
            'step_1': 'Login at /api/auth/login/ with demo credentials',
            'step_2': 'Copy the access token from response',
            'step_3': 'Add header: Authorization: Bearer YOUR_TOKEN',
            'step_4': 'Try any endpoint or visit /api/docs/ for interactive testing'
        }
    })


# Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Finance Dashboard API",
        default_version='v1',
        description="Backend API for Finance Dashboard with Role-Based Access Control",
        contact=openapi.Contact(email="admin@finance.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Root
    path('api/', api_root, name='api-root'),
    
    # API Documentation (Swagger)
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    path('api/auth/', include('users.urls')),
    path('api/users/', include('users.urls')),
    path('api/records/', include('finance.urls')),
    path('api/dashboard/', include('dashboard.urls')),
]