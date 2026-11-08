# Olist E-Commerce Sales & Delivery Analytics

End-to-end analytics project: **Python + MySQL + Power BI** on the Brazilian Olist e-commerce dataset (about 100k orders, 8 relational tables).

## Business questions
1. How are revenue, orders and average order value trending?
2. Which categories, sellers and states drive revenue?
3. Who are the high-value customers, and how many buy again?
4. Are deliveries on time, and how does delay affect review scores?

## Architecture
```
Kaggle CSVs -> Python (clean + load) -> MySQL staging
            -> stored procedure (fact/dim star schema)
            -> Python (RFM + K-Means) -> MySQL -> Power BI
```

## Tech stack
- **Python:** pandas, SQLAlchemy, PyMySQL, scikit-learn
- **MySQL 8:** multi-table joins, indexes, stored procedure `sp_refresh_marts`
- **Power BI Desktop:** star-schema model, DAX time intelligence (YoY, MoM, YTD), slicers, KPI cards

## Dashboard
### Executive Overview
![Executive Overview](screenshots/page1_overview.png)
### Delivery & Satisfaction
![Delivery and Satisfaction](screenshots/page2_delivery.png)
### Customers
![Customers](screenshots/page3_customers.png)
### Products & Sellers
![Products and Sellers](screenshots/page4_products.png)

## Key insights
- **Scale:** about 99,441 orders and about 13.5M in revenue across the dataset.
- **Delivery hurts ratings:** orders delivered on time average about 4.3 stars, while orders late by 1 to 7 days drop to about 2.7 and orders more than 7 days late to about 1.7.
- **Delivery performance:** for 2018, about 94.6% of orders arrived on or before the estimated date, with an average delivery time of about 12 days. Far-north states (RR, AM, AP) take roughly 26 to 28 days.
- **Retention is the gap:** only about 3% of customers place a second order, so repeat purchase is the biggest growth opportunity.
- **Concentration:** Sao Paulo (SP) is the largest state by revenue and customers, well ahead of RJ and MG.

## Customer segmentation
Customers were scored on recency, frequency and monetary value (RFM), then clustered with K-Means (k=4, log-scaled and standardised). Most customers buy once, so frequency varies little. The segments are named from the cluster profiles: Lapsed High Spenders, Lapsed Low Spenders, Recent Low Spenders and Repeat Buyers.

## How to run
1. Download the dataset from Kaggle ("Brazilian E-Commerce Public Dataset by Olist") into `data/raw/`.
2. Install MySQL 8 and set your password in `python/config.py` (or the `DB_PASSWORD` environment variable).
3. `pip install -r requirements.txt`
4. `python run_all.py`
5. Open Power BI Desktop, connect to MySQL (`localhost`, database `olist`), and load `powerbi/olist_dashboard.pbix`. DAX is in `powerbi/measures.dax`.

## Notes
- The customer count on the Customers page (about 96K) is higher than the segmented count (about 93K), because segmentation uses delivered orders only.
- Olist data starts in Sep 2016 with very low volume, so year-over-year comparisons are only meaningful for 2018 versus 2017 (Jan to Aug).
