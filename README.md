# Olist E-Commerce Sales & Delivery Analytics
Python + MySQL + Power BI project on the Olist Brazilian E-Commerce dataset (~100k orders, 9 tables).

## Run
1. Download the dataset from Kaggle ("Brazilian E-Commerce Public Dataset by Olist") and put all CSVs in `data/raw/`.
2. Install MySQL 8 and start it. Edit the password in `python/config.py` (or set DB_PASSWORD).
3. `pip install -r requirements.txt`
4. `python run_all.py`   (loads staging -> builds star schema via stored procedure -> RFM segmentation)
5. Open Power BI Desktop and follow `powerbi/POWERBI_GUIDE.md`; DAX is in `powerbi/measures.dax`.

## Pipeline
CSV -> Python (clean/load) -> MySQL staging -> stored procedure `sp_refresh_marts` (fact/dim tables) -> Python K-Means RFM -> MySQL -> Power BI.

## Key insights
(Fill in after building the dashboard: revenue growth, top categories, repeat-customer %, on-time % and its effect on review score.)
