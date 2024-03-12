from django.urls import path
from .views import *


urlpatterns = [
    path('getS3UploadUrl', S3UploadUrlView.as_view()),
    path('getAwsSignedCookies', GetAwsSignedCookiesView.as_view()),
]