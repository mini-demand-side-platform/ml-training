from abc import ABC, abstractmethod
from io import BytesIO

from minio import Minio

from .config import DBServerInfo


class ObjectStorage(ABC):
    @abstractmethod
    def save(self):
        pass


class MinioObjectStorage(ObjectStorage):
    def __init__(self, db_server_info: DBServerInfo) -> None:
        self._db_server_info = db_server_info

    def save(self, bucket_name: str, bytes_data: BytesIO):
        Minio(
            endpoint=self._db_server_info.host + ":" + self._db_server_info.port,
            access_key=self._db_server_info.username,
            secret_key=self._db_server_info.password,
            secure=False,
        )
