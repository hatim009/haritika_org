from rest_framework import viewsets
from .serializers import FarmerSerializer
from .models import Farmer


class FarmerViewSet(viewsets.ModelViewSet):
    serializer_class = FarmerSerializer
    queryset = Farmer.objects.all()

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user, last_edited_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(last_edited_by=self.request.user)
