from uuid_extensions import uuid7str
from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework import views, status
from rest_framework.response import Response

from .utils import generate_presigned_url, generate_presigned_post, S3Url


class S3UploadUrlView(views.APIView):
    
    def get(self, request):
        s3_key = "resources/files/" + request.data.get('key', uuid7str())
        
        url = generate_presigned_post(settings.HARITIKA_ORG_S3_BUCKET, s3_key)
        
        return Response(url)


class S3DownloadUrlView(views.APIView):

    def get(self, request):
        try:
            s3_url = S3Url(request.data.get('s3_path'))
            url = generate_presigned_url(s3_url.bucket, s3_url.key)
            return Response(url)
        except ValidationError as e:
            return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)