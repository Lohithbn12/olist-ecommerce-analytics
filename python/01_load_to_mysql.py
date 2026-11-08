"""Step 1: create the database, then load the raw CSVs into MySQL staging tables."""
import pandas as pd
from sqlalchemy import text, types
from config import get_engine, RAW, DB_NAME

with get_engine(with_db=False).begin() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))

engine = get_engine()

files = {
    "stg_customers": "olist_customers_dataset.csv",
    "stg_orders": "olist_orders_dataset.csv",
    "stg_order_items": "olist_order_items_dataset.csv",
    "stg_payments": "olist_order_payments_dataset.csv",
    "stg_reviews": "olist_order_reviews_dataset.csv",
    "stg_products": "olist_products_dataset.csv",
    "stg_sellers": "olist_sellers_dataset.csv",
    "stg_category_translation": "product_category_name_translation.csv",
}

for table, fname in files.items():
    path = RAW / fname
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Download the Olist dataset into data/raw/")
    df = pd.read_csv(path).drop_duplicates()

    for col in df.columns:
        if "date" in col or "timestamp" in col or col.endswith("_at"):
            df[col] = pd.to_datetime(df[col], errors="coerce")

    if table == "stg_products":
        df = df.rename(columns={"product_name_lenght": "product_name_length",
                                "product_description_lenght": "product_description_length"})
        df["product_category_name"] = df["product_category_name"].fillna("unknown")
    if table == "stg_reviews":
        df = df.drop(columns=["review_comment_title", "review_comment_message"])
        df = df.drop_duplicates(subset=["review_id", "order_id"])

    dtype = {c: types.String(50) for c in df.columns if c.endswith("_id")}
    for c in ("product_category_name", "product_category_name_english"):
        if c in df.columns:
            dtype[c] = types.String(100)

    df.to_sql(table, engine, if_exists="replace", index=False, dtype=dtype, chunksize=5000)
    print(f"{table}: {len(df):,} rows loaded")

print("Staging load complete.")
