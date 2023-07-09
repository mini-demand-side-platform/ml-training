from abc import ABC, abstractmethod

import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split

from .config import DBServerInfo
from .logger import get_logger

log = get_logger(logger_name="data_pipeline")


class DataPipeline(ABC):
    @abstractmethod
    def get_training_data(self):
        pass

    @abstractmethod
    def get_testing_data(self):
        pass


class PostgresDataPipeline(DataPipeline):
    def __init__(
        self,
        db_server_info: DBServerInfo,
        feature_table_name: str,
        label_table_name: str,
        label_column_name: str,
    ) -> None:
        self._db_server_info = db_server_info
        conn = self._get_connection()
        cur = conn.cursor()

        # Execute a query
        cur.execute(
            "SELECT * FROM {feature_table_name}".format(
                feature_table_name=feature_table_name
            )
        )

        # Retrieve query results
        records = cur.fetchall()
        X = pd.DataFrame(records)

        cur.execute(
            "SELECT {label_column_name} FROM {label_table_name}".format(
                label_column_name=label_column_name, label_table_name=label_table_name
            )
        )

        records = cur.fetchall()
        y = pd.DataFrame(records)
        cur.close()
        conn.close()
        # index 0 in X is the row id
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X.drop(0, axis=1), y, test_size=0.33, random_state=42
        )

    def _get_connection(self) -> psycopg2.extensions.connection:
        """_summary_

        Returns:
            psycopg2.extensions.connection: _description_
        """
        return psycopg2.connect(
            host=self._db_server_info.host,
            port=self._db_server_info.port,
            database=self._db_server_info.database,
            user=self._db_server_info.username,
            password=self._db_server_info.password,
        )

    def get_training_data(self):
        return self.X_train, self.y_train

    def get_testing_data(self):
        return self.X_test, self.y_test


class CSVFileDataPipeline(DataPipeline):
    def get_training_data(self):
        pass

    def get_testing_data(self):
        pass
