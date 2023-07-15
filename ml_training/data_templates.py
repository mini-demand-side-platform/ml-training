from dataclasses import dataclass


@dataclass
class DBServerInfo:
    host: str
    port: str
    database: str
    username: str
    password: str
