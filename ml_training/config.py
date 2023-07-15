import os

from data_templates import DBServerInfo

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
    port=os.getenv("object_storage_info", "9000"),
    database=os.getenv("object_storage_database", "object"),
    username=os.getenv("object_storage_username", "dsp"),
    password=os.getenv("object_storage_password", "dsppassword"),
)

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
