from rest_framework import views, status
from rest_framework.response import Response
from .serializers import *
from .models import *


class StatesDirectoryView(views.APIView):
    
    def get(self, request):
        states_directory = StatesDirectory.objects.all()
        states_directory_serializer = StatesDirectorySerializer(states_directory, many=True)
        return Response({'statesDirectory': states_directory_serializer.data})


class DistrictsDirectoryView(views.APIView):
    
    def get(self, request, state_code):
        districts_directory = DistrictsDirectory.objects.filter(state=state_code)
        if districts_directory.exists():
            districts_directory_serializer = DistrictsDirectorySerializer(districts_directory, many=True)
            return Response({'districtsDirectory': districts_directory_serializer.data})
        
        return Response('state_code %s not found.' % state_code, status=status.HTTP_404_NOT_FOUND)


class BlocksDirectoryView(views.APIView):
    
    def get(self, request, district_code):
        blocks_directory = BlocksDirectory.objects.filter(district=district_code)
        if blocks_directory.exists():
            blocks_directory_serializer = BlocksDirectorySerializer(blocks_directory, many=True)
            return Response({'blocksDirectory': blocks_directory_serializer.data})
        
        return Response('district_code %s not found.' % district_code, status=status.HTTP_404_NOT_FOUND)


class VillagesDirectoryView(views.APIView):
    
    def get(self, request, block_code):
        villages_directory = VillagesDirectory.objects.filter(block=block_code)
        if villages_directory.exists():
            villages_directory_serializer = VillagesDirectorySerializer(villages_directory, many=True)
            return Response({'villagesDirectory': villages_directory_serializer.data})
        
        return Response('block_code %s not found.' % block_code, status=status.HTTP_404_NOT_FOUND)