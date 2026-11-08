"""Step 3: RFM + K-Means customer segmentation, written back to MySQL."""
import pandas as pd, numpy as np
from sqlalchemy import types
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from config import get_engine

engine = get_engine()

q = """
SELECT f.customer_unique_id,
       MAX(f.order_date)          AS last_order,
       COUNT(DISTINCT f.order_id) AS frequency,
       SUM(i.price)               AS monetary
FROM fact_orders f
JOIN fact_order_items i ON i.order_id = f.order_id
WHERE f.order_status = 'delivered'
GROUP BY f.customer_unique_id
"""
df = pd.read_sql(q, engine, parse_dates=["last_order"])

snapshot = df["last_order"].max() + pd.Timedelta(days=1)
df["recency"] = (snapshot - df["last_order"]).dt.days

X = StandardScaler().fit_transform(np.log1p(df[["recency", "frequency", "monetary"]]))
df["cluster"] = KMeans(n_clusters=4, n_init=10, random_state=42).fit_predict(X)

profile = df.groupby("cluster")[["recency", "frequency", "monetary"]].mean().round(1)
print(profile)

# Data-driven labels, based on each cluster's position vs the median of the cluster means
med_r, med_m = profile["recency"].median(), profile["monetary"].median()
labels, seen = {}, {}
for c, row in profile.iterrows():
    if row["frequency"] > 1.2:
        name = "Repeat Buyers"
    else:
        r = "Recent" if row["recency"] <= med_r else "Lapsed"
        m = "High Spenders" if row["monetary"] >= med_m else "Low Spenders"
        name = f"{r} {m}"
    seen[name] = seen.get(name, 0) + 1
    labels[c] = name if seen[name] == 1 else f"{name} {seen[name]}"
df["segment"] = df["cluster"].map(labels)
print(df["segment"].value_counts())

df[["customer_unique_id", "recency", "frequency", "monetary", "segment"]].to_sql(
    "customer_segments", engine, if_exists="replace", index=False,
    dtype={"customer_unique_id": types.String(50)}, chunksize=5000)
print("customer_segments written.")
