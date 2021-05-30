from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from bernini.serializers import UserSerializer, PasswordSerializer, UserDetailSerializer
from bernini.permissions import IsUserOwner, IsAdminUser

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminUser | IsUserOwner]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'set_password':
            return PasswordSerializer
        elif self.action == 'partial_update' or self.action == 'update':
            return UserDetailSerializer
        return UserSerializer

    @action(detail=True, methods=['post'], url_name="change_password")
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            if check_password(serializer.validated_data['old_password'], user.password):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({'status': 'password set'})
            else:
                return Response({'status': 'old password is wrong'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)