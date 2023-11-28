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
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user.is_active = False
            user.save()
            return Response({'status': 'User marked as inactive'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    """
    Assign a block to a User.
    """
    @action(detail=True, methods=['post'], url_path='blocks/(?P<block_code>[^/.]+)', permission_classes=(IsAdmin,))
    def block(self, request, pk=None, block_code=None, **kwargs):
        user_block_serializer = UserBlockSerializer(data={'user':pk, 'block':block_code})
        if user_block_serializer.is_valid():
            user_block_serializer.save()
            return Response({'status': 'block assigned successfully'})
        
        return Response(user_block_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    """
    Remove a block from a User.
    """
    @block.mapping.delete
    def removeBlock(self, request, pk=None, block_code=None, **kwargs):
        try:
            user_block = UserBlock.objects.get(user=pk, block=block_code)
            user_block.delete()
        except UserBlock.DoesNotExist:
            pass

        return Response({'status': 'block successfully removed.'})
            
        
