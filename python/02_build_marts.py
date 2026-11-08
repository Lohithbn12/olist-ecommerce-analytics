"""Step 2: create indexes, build the stored procedure, run it, validate."""
import pandas as pd
from sqlalchemy import text
from config import get_engine, SQL_DIR

engine = get_engine()


def strip_comments(sql):
    return "\n".join(l for l in sql.splitlines() if not l.strip().startswith("--"))


# indexes (ignore 'duplicate index' errors on re-run)
for stmt in strip_comments((SQL_DIR / "01_indexes.sql").read_text()).split(";"):
    stmt = stmt.strip()
    if not stmt:
        continue
    try:
        with engine.begin() as conn:
            conn.execute(text(stmt))
    except Exception as e:
        if "Duplicate key name" not in str(e):
            raise

# stored procedure: remove comments first, then split DROP from CREATE
proc_sql = strip_comments((SQL_DIR / "02_stored_procedure.sql").read_text())
drop_part, create_part = proc_sql.split("CREATE PROCEDURE", 1)
drop_stmt = drop_part.strip().rstrip(";")
create_stmt = "CREATE PROCEDURE" + create_part

# raw DBAPI connection so semicolons inside the procedure body stay intact
raw = engine.raw_connection()
try:
    cur = raw.cursor()
    cur.execute(drop_stmt)
    cur.execute(create_stmt.strip())
    cur.execute("CALL sp_refresh_marts()")
    raw.commit()
finally:
    raw.close()

print("fact_orders rows   :", pd.read_sql("SELECT COUNT(*) n FROM fact_orders", engine)["n"][0])
print("distinct order_ids :", pd.read_sql("SELECT COUNT(DISTINCT order_id) n FROM fact_orders", engine)["n"][0])
print("total revenue      :", pd.read_sql("SELECT ROUND(SUM(price)) s FROM fact_order_items", engine)["s"][0])
print("Marts built.")