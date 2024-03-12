from uuid_extensions import uuid7str

from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework import views, status
from rest_framework.response import Response

from .utils import (generate_presigned_post, get_cloudfront_policy, get_cloudfront_signature, aws_b64encode)


class S3UploadUrlView(views.APIView):
    
    def get(self, request):
        s3_key = "resources/files/" + request.query_params.get('key', uuid7str())
        
        url = generate_presigned_post(settings.STATIC_HARITIKA_ORG_S3_BUCKET, s3_key)
        url['resource_url'] = 'https://{cloudfront_domain}/{resource_key}'.format(
            cloudfront_domain=settings.AWS_CLOUDFRONT_DOMAIN, resource_key=s3_key)

        return Response(url)


class GetAwsSignedCookiesView(views.APIView):
    def get(self, request):
        cloudfront_policy = get_cloudfront_policy()
        cloudfront_signature = get_cloudfront_signature(cloudfront_policy.encode('utf-8'))
        cloudfront_key_pair_id = settings.AWS_CLOUDFRONT_KEY_PAIR_ID

        return Response({
            'awsSignedCookies': {
                'CloudFront-Policy': aws_b64encode(cloudfront_policy.encode('utf-8 ')),
                'CloudFront-Signature': aws_b64encode(cloudfront_signature),
                'CloudFront-Key-Pair-Id': cloudfront_key_pair_id
            }
        })
