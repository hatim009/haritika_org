from rest_framework import views
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .serializers import StatesDirectorySerializer, DistrictsDirectorySerializer, BlocksDirectorySerializer, VillagesDirectorySerializer
from .models import StatesDirectory, DistrictsDirectory, BlocksDirectory, VillagesDirectory


class StatesDirectoryView(views.APIView):
    
    def get(self, request):
        states_directory = StatesDirectory.objects.all()
        states_directory_serializer = StatesDirectorySerializer(states_directory, many=True)
        return Response({'statesDirectory': states_directory_serializer.data})


class DistrictsDirectoryView(views.APIView):
    
    def get(self, request, state_code):
        districts_directory = DistrictsDirectory.objects.filter(state_code=state_code)
        districts_directory_serializer = DistrictsDirectorySerializer(districts_directory, many=True)
        return Response({'districtsDirectory': districts_directory_serializer.data})


class BlocksDirectoryView(views.APIView):
    
    def get(self, request, district_code):
        blocks_directory = BlocksDirectory.objects.filter(district_code=district_code)
        blocks_directory_serializer = BlocksDirectorySerializer(blocks_directory, many=True)
        return Response({'blocksDirectory': blocks_directory_serializer.data})


class VillagesDirectoryView(views.APIView):
    
    def get(self, request, block_code):
        villages_directory = VillagesDirectory.objects.filter(block_code=block_code)
        villages_directory_serializer = VillagesDirectorySerializer(villages_directory, many=True)
        return Response({'villagesDirectory': villages_directory_serializer.data})