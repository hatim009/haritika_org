from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from users.permissions import IsSupervisor, IsSurveyor
from users.filters import UserFilter
from users.models import User, UserBlock
from users.serializers import UserSerializer, PasswordSerializer

from permissions import  IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin|IsSupervisor|IsSurveyor]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    search_fields = ['name', 'phone_number']
    filterset_class = UserFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        
        if self.action == 'list':
            queryset = queryset.filter(is_active=True).exclude(id=self.request.user.id)
            
            match self.request.user.user_type:
                case User.UserType.SURVEYOR:
                    raise PermissionDenied("You do not have permission to perform this action.")
            
                case User.UserType.SUPERVISOR:
                    assigned_blocks = [user_block.block.code for user_block in self.request.user.assigned_blocks.all()]
                    surveyors_in_assigned_blocks = [user_block.user.id for user_block in UserBlock.objects.filter(block__in=assigned_blocks).filter(user__user_type=User.UserType.SURVEYOR).distinct('user')]
                    queryset = queryset.filter(id__in=surveyors_in_assigned_blocks)

        return queryset

    @action(detail=False, methods=['GET'], name='Get User Profile')
    def profile(self, request, *args, **kwargs):
        return Response(UserSerializer(self.request.user).data)

    @action(detail=True, methods=['put'], name='Change Password')
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
    
    @action(detail=True, methods=['put'], name='Activate User')
    def activate(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'User activated successfully.'})

    @action(detail=True, methods=['put'], name='Deactivate User')
    def deactivate(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'User deactivated successfully.'})