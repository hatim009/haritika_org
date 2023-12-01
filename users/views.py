from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import IsAdmin, IsAdminOrSelf
from .models import User, UserBlock
from .serializers import UserSerializer, PasswordSerializer, UserBlockSerializer
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=True, methods=['put'], name='Change Password', 
            permission_classes=(IsAdminOrSelf,))
    def password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'User marked as inactive'})
        
            
        
