from io import StringIO, BytesIO
from typing import Union

import boto3
import logging
import pandas as pd
import pandas.core.frame

from xetra.common.constants import S3FileTypes
from xetra.common.custom_exceptions import WrongFormatException


class S3BucketConnector:
    """
    Class for interacting with S3 Buckets
    """

    def __init__(
        self, access_key: str, secret_key: str, endpoint_url: str, bucket: str
    ):
        """
        Constructor for S3BucketConnector

        :param access_key: access key for accessing S3
        :param secret_key: secret key for accessing S33
        :param endpoint_url: endpoint url to S3
        :param bucket: S3 bucket name
        """
        self._logger = logging.getLogger(__name__)
        self.access_key = access_key
        self.secret_key = secret_key
        self.end_point_url = endpoint_url
        self.session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )
        self._s3 = self.session.resource(
            service_name="s3", endpoint_url=endpoint_url
        )
        self._bucket = self._s3.Bucket(bucket)

    def list_files_in_prefix(self, prefix: str):
        """Listing all files with a prefix on the S3 bucket

        :param prefix: prefix on the S3 bucket that should be filtered with
        :return:
            files: list of all the file names containing the prefix in the key
        """
        files = [obj.key for obj in self._bucket.objects.filter(Prefix=prefix)]
        return files

    def read_csv_to_df(
        self, key: str, encoding: str = "utf-8", sep: str = ","
    ) -> pandas.core.frame.DataFrame:
        """
        reading a csv file from the S3 bucket and returning a dataframe
        :param key: key of the file that should be read
        :param encoding: encoding of the data inside the csv file
        :param sep: separator of the csv file
        :return:
            data_frame: Pandas DataFrame containing the data of the csv file
        """
        self._logger.info(
            "Reading file %s/%s/%s", self.end_point_url, self._bucket.name, key
        )
        csv_obj = (
            self._bucket.Object(key=key)
            .get()
            .get("Body")
            .read()
            .decode(encoding)
        )
        data = StringIO(csv_obj)
        data_frame = pd.read_csv(data, sep=sep)
        return data_frame

    def write_df_to_s3(
        self,
        data_frame: pandas.core.frame.DataFrame,
        key: str,
        file_format: str,
    ):
        """
        writing a Pandas DataFrame to S3
        :param data_frame: Pandas DataFrame that should be written
        :param key: target key of the saved file
        :param file_format: format of the saved file
        :return:
        """
        if data_frame.empty:
            self._logger.info(
                "The dataframe is empty! No file will be written!"
            )
            return None

        if file_format == S3FileTypes.CSV.value:
            out_buffer = StringIO()
            data_frame.to_csv(out_buffer, index=False)
            return self.__put_object(out_buffer, key)

        if file_format == S3FileTypes.PARQUET.value:
            out_buffer = BytesIO()
            data_frame.to_parquet(out_buffer, index=False)
            return self.__put_object(out_buffer, key)

        self._logger.info(
            "The file format %s is not supported to be written to s3!",
            file_format,
        )
        raise WrongFormatException

    def __put_object(
        self, out_buffer: Union[StringIO, BytesIO], key: str
    ) -> bool:
        """
        Helper function for self.write_df_to_s3()

        :param out_buffer: StringIO | BytesIO that should be written
        :param key: target key of the saved file
        """
        self._logger.info(
            "Writing file to %s/%s/%s",
            self.end_point_url,
            self._bucket.name,
            key,
        )
        self._bucket.put_object(Body=out_buffer.getvalue(), Key=key)
        return True
