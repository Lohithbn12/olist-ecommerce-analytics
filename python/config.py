import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Edit these, or set them as environment variables
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "YOUR_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "olist")

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
SQL_DIR = ROOT / "sql"


def get_engine(with_db=True):
    url = URL.create(
        "mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME if with_db else None,
    )
    return create_engine(url)