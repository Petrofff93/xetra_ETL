import unittest
from datetime import datetime, timedelta

import boto3
from moto import mock_s3

from xetra.common.constants import MetaProcessFormat
from xetra.common.s3 import S3BucketConnector


class TestMetaProcessMethods(unittest.TestCase):
    """
    Testing the MetaProcess class.
    """

    def setUp(self) -> None:
        """
        Setting up the environment
        """
        # mocking s3 connection start
        self.mock_s3 = mock_s3()
        self.mock_s3.start()
        # Defining the class arguments
        self.s3_access_key = 'AWS_ACCESS_KEY_ID'
        self.s3_secret_key = 'AWS_SECRET_ACCESS_KEY'
        self.s3_endpoint_url = 'https://s3.eu-central-1.amazonaws.com'
        self.s3_bucket_name = 'test_bucket'
        # Creating a bucket on the mocked s3
        self.s3 = boto3.resource(service_name='s3', endpoint_url=self.s3_endpoint_url)
        self.s3.create_bucket(Bucket=self.s3_bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-central-1'})
        self.s3_bucket = self.s3.Bucket(self.s3_bucket_name)
        # Creating a S3BucketConnector instance
        self.s3_bucket_meta = S3BucketConnector(self.s3_access_key, self.s3_secret_key, self.s3_endpoint_url, self.s3_bucket_name)
        self.dates = [(datetime.today().date() - timedelta(days=day)).strftime(MetaProcessFormat.META_DATE_FORMAT.value) for day in range(8)]

    def tearDown(self) -> None:
        # mocking s3 connection stop
        self.mock_s3.stop()


