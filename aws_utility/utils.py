import logging
from urllib.parse import urlparse
from botocore.exceptions import ClientError

from django.conf import settings
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = settings.BOTO_S3_CLIENT
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def generate_presigned_post(bucket_name, object_name, fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """
    s3_client = settings.BOTO_S3_CLIENT
    try:
        url = s3_client.generate_presigned_post(bucket_name, 
                                                object_name, 
                                                Fields=fields, 
                                                Conditions=conditions, 
                                                ExpiresIn=expiration)
        logger.info("Got presigned URL: %s", url)
    except ClientError as e:
        logging.error(e)
        raise
    return url


class S3Url(object):
    """
        >>> s = S3Url("s3://bucket/hello/world")
        >>> s.bucket
        'bucket'
        >>> s.key
        'hello/world'
        >>> s.url
        's3://bucket/hello/world'

        >>> s = S3Url("s3://bucket/hello/world?qwe1=3#ddd")
        >>> s.bucket
        'bucket'
        >>> s.key
        'hello/world?qwe1=3#ddd'
        >>> s.url
        's3://bucket/hello/world?qwe1=3#ddd'

        >>> s = S3Url("s3://bucket/hello/world#foo?bar=2")
        >>> s.key
        'hello/world#foo?bar=2'
        >>> s.url
        's3://bucket/hello/world#foo?bar=2'
    """

    def __init__(self, url):
        self._parsed = urlparse(url, allow_fragments=False)
        if 's3' != self._parsed.scheme or not self.bucket or not self.key:
            raise ValidationError('Invalid s3 url: {0}'.format(url))

    @property
    def bucket(self):
        return self._parsed.netloc

    @property
    def key(self):
        if self._parsed.query:
            return self._parsed.path.lstrip('/') + '?' + self._parsed.query
        else:
            return self._parsed.path.lstrip('/')

    @property
    def url(self):
        return self._parsed.geturl()
