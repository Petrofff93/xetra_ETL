import boto3


class S3BucketConnector:
    """
    Class for interacting with S3 Buckets
    """

    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket: str):
        """
        Constructor for S3BucketConnector

        :param access_key: access key for accessing S3
        :param secret_key: secret key for accessing S33
        :param endpoint_url: endpoint url to S3
        :param bucket: S3 bucket name
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.end_point_url = endpoint_url
        self.session = boto3.Session(aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        self._s3 = self.session.resource(service_name='s3', endpoint_url=endpoint_url)
        self._bucket = self._s3.Bucket(bucket)

    def list_files_in_prefix(self):
        pass

    def read_csv_to_df(self):
        pass

    def write_df_to_s3(self):
        pass
