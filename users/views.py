"""
API views for User management and authentication.
"""
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login

from .models import User
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    LoginSerializer,
    PasswordChangeSerializer
)
from .permissions import IsAdmin, IsOwnerOrAdmin


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Public endpoint - no authentication required.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Register new user and return tokens."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
    API endpoint for user login.
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Authenticate user and return JWT tokens."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user management.
    
    list:   GET /api/users/ - List all users (Admin only)
    create: POST /api/users/ - Create user (Admin only)
    retrieve: GET /api/users/{id}/ - Get user details
    update: PUT /api/users/{id}/ - Update user
    partial_update: PATCH /api/users/{id}/ - Partial update
    destroy: DELETE /api/users/{id}/ - Deactivate user (Admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['list', 'create', 'destroy']:
            # Only admins can list all users, create, or delete
            return [IsAdmin()]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            # Users can view/update own profile, admins can view/update any
            return [IsOwnerOrAdmin()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        """Use different serializers for different actions."""
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user role.
        Admins see all users, others see only themselves.
        """
        user = self.request.user
        
        if user.is_admin:
            return User.objects.all()
        else:
            return User.objects.filter(id=user.id)
    
    def destroy(self, request, *args, **kwargs):
        """
        Soft delete - deactivate user instead of deleting.
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(
            {'message': 'User deactivated successfully'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        GET /api/users/me/
        Get current user's profile.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def activate(self, request, pk=None):
        """
        POST /api/users/{id}/activate/
        Activate a deactivated user (Admin only).
        """
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response(
            {'message': 'User activated successfully'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """
        POST /api/users/change-password/
        Change current user's password.
        """
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Password changed successfully'},
            status=status.HTTP_200_OK
        )