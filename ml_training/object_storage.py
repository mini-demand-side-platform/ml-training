from abc import ABC, abstractmethod
from io import BytesIO

from minio import Minio

from .config import DBServerInfo
from .logger import get_logger

log = get_logger(logger_name="object_storage")


class ObjectStorage(ABC):
    @abstractmethod
    def save(self):
        pass


class MinioObjectStorage(ObjectStorage):
    def __init__(self, db_server_info: DBServerInfo) -> None:
        self._db_server_info = db_server_info

    def save(
        self, bucket_name: str, object_name: str, bytes_data: BytesIO, data_length: int
    ) -> None:
        conn = Minio(
            endpoint=self._db_server_info.host + ":" + self._db_server_info.port,
            access_key=self._db_server_info.username,
            secret_key=self._db_server_info.password,
            secure=False,
        )
        if not conn.bucket_exists(bucket_name):
            conn.make_bucket(bucket_name)
        conn.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=bytes_data,
            length=data_length,
        )
