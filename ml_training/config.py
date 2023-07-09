import os
from dataclasses import dataclass


@dataclass
class DBServerInfo:
    host: str
    port: str
    database: str
    username: str
    password: str


olap_server_info = DBServerInfo(
    host=os.getenv("olap_host", "localhost"),
    port=os.getenv("olap_port", "5432"),
    database=os.getenv("olap_database", "olap"),
    username=os.getenv("olap_username", "dsp"),
    password=os.getenv("postgres_password", "dsppassword"),
)

cache_server_info = DBServerInfo(
    host=os.getenv("cache_host", "localhost"),
    port=os.getenv("cache_port", "6379"),
    database=os.getenv("cache_database", "cache"),
    username=os.getenv("cache_username", "dsp"),
    password=os.getenv("cache_password", "dsppassword"),
)
object_storage_server_info = DBServerInfo(
    host=os.getenv("object_storage_host", "localhost"),
    port=os.getenv("object_storage_info", "localhost"),
    database=os.getenv("object_storage_info", "localhost"),
    username=os.getenv("minio_access_key", "dsp"),
    password=os.getenv("minio_secret_key", "dsppassword"),
)

train_method = os.getenv("train_method", "sklearn")
data_pipeline_method = os.getenv("data_pipeline_method", "postgres")
model_saver_method = os.getenv("model_saver_method", "minio")

minio_server_info = {
    "uri": os.getenv("minio_uri", "localhost:9000"),
    "access_key": os.getenv("minio_access_key", "dsp"),
    "secret_key": os.getenv("minio_secret_key", "dsppassword"),
}

data_columns = [
    "ad_id",
    "status",
    "bidding_cpc",
    "advertiser",
    "banner_style",
    "category",
    "height",
    "width",
    "item_price",
    "layout_style",
    "hist_ctr",
    "hist_cvr",
    "was_click",
]


target_features = "was_click"
