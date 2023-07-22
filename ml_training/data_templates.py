from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class DBServerInfo:
    host: str
    port: str
    database: str
    username: str
    password: str


class TrainModelInput(BaseModel):
    feature_table_name: str
    label_table_name: str
    label_column_name: str
