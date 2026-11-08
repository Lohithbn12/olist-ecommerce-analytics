# Olist E-Commerce Sales & Delivery Analytics

An end-to-end analytics project built with **Python, MySQL and Power BI** on the public Brazilian Olist e-commerce dataset (about 100k orders, 8 relational tables). Raw CSVs go through a cleaning and loading pipeline into MySQL, a stored procedure builds a star schema, a clustering model segments customers, and a 4-page Power BI dashboard reports the results.

## Business questions
1. How are revenue, orders and average order value trending, and how does this year compare with last?
2. Which product categories, sellers and states drive revenue?
3. Who are the high-value customers, and how many come back to buy again?
4. Are orders delivered on time, and how does delay affect review scores?

## Tech stack
| Layer | Tools |
|---|---|
| Data cleaning and loading | Python (pandas, SQLAlchemy, PyMySQL) |
| Storage and modelling | MySQL 8: joins, indexes, stored procedure |
| Customer segmentation | Python (scikit-learn): RFM + K-Means |
| Reporting | Power BI Desktop: data model, DAX, slicers, KPI cards |

## Architecture
```
Kaggle CSVs
   -> Python (clean, type-cast, load)        01_load_to_mysql.py
   -> MySQL staging tables (stg_*)
   -> Stored procedure sp_refresh_marts()    02_build_marts.py
   -> Star schema (fact_* and dim_* tables)
   -> Python RFM + K-Means                   03_rfm_segmentation.py
   -> customer_segments table
   -> Power BI (import mode)
```

## Data model (star schema)
| Table | Grain | Purpose |
|---|---|---|
| `fact_orders` | one row per order | status, dates, delivery days, delay days, payment value, review score |
| `fact_order_items` | one row per item | price, freight, product and seller keys |
| `dim_product` | one row per product | English category name, weight, photos |
| `dim_seller` | one row per seller | city, state |
| `dim_customer` | one row per unique customer | city, state |
| `customer_segments` | one row per customer | recency, frequency, monetary, segment |
| `dim_date` | one row per day | built in Power BI with DAX |

## Dashboard pages
1. **Executive Overview:** revenue, orders, AOV and YoY growth cards; monthly revenue against last year; top 10 states by revenue; Year and Month slicers.
2. **Delivery & Satisfaction:** on-time delivery %, average delivery days, average review score; review score by delay bucket; slowest states; monthly on-time trend.
3. **Customers:** total and repeat customers, repeat rate, revenue per customer; segment mix; RFM profile table; customers by state.
4. **Products & Sellers:** revenue and freight KPIs; top 10 categories; category treemap; revenue vs freight scatter; top 10 sellers.

## Key DAX measures
Total Revenue, Total Orders, AOV, Revenue LY, Revenue YoY %, Revenue MoM %, Revenue YTD, On-Time Delivery %, Avg Delivery Days, Avg Review Score, Repeat Customers, Repeat Customer %, Revenue per Customer, Freight % of Revenue. All are in `powerbi/measures.dax`.

## Key findings
- **Scale:** 99,441 orders and about 13.5M in item revenue (Sep 2016 to Oct 2018).
- **Late delivery hurts ratings:** orders delivered on time or early average about 4.3 stars, orders 1 to 7 days late fall to about 2.7, and orders more than 7 days late fall to about 1.7.
- **Delivery performance (2018):** about 94.6% of orders arrived by the estimated date, with an average delivery time of about 12 days and an average review of about 4.1.
- **Geography:** the far-north states (RR, AM, AP) wait about 26 to 28 days on average, more than double the overall average.
- **Retention is the main gap:** only about 3% of customers place a second order. Repeat buyers number about 2.8k out of about 93k delivered-order customers.
- **Concentration:** Sao Paulo (SP) leads revenue and customer count by a wide margin over RJ and MG.

## Customer segmentation
Each customer is scored on **recency** (days since last delivered order), **frequency** (orders) and **monetary** value (item revenue). Features are log-transformed and standardised, then clustered with K-Means (k = 4). Because most customers buy only once, frequency varies little, so recency and spend drive the clusters. Segments are named from the cluster profiles: Lapsed High Spenders, Lapsed Low Spenders, Recent Low Spenders and Repeat Buyers.

## Repository structure
```
olist-ecommerce-analytics/
├── data/raw/                 (place Kaggle CSVs here; not tracked)
├── python/
│   ├── config.py             database connection settings
│   ├── 01_load_to_mysql.py   clean CSVs and load staging tables
│   ├── 02_build_marts.py     indexes, stored procedure, validation
│   └── 03_rfm_segmentation.py
├── sql/
│   ├── 01_indexes.sql
│   ├── 02_stored_procedure.sql
│   └── 03_validation.sql
├── powerbi/
│   ├── olist_dashboard.pbix
│   ├── measures.dax
│   └── POWERBI_GUIDE.md
├── requirements.txt
├── run_all.py
└── README.md
```

## How to run
1. Download the dataset from Kaggle ("Brazilian E-Commerce Public Dataset by Olist") and put the CSV files in `data/raw/`.
2. Install MySQL 8 and start the server.
3. Set your password in `python/config.py`, or set the `DB_PASSWORD` environment variable.
4. Install dependencies: `pip install -r requirements.txt`
5. Run the pipeline: `python run_all.py`
6. Open `powerbi/olist_dashboard.pbix` in Power BI Desktop. If asked, point the MySQL source at `localhost` and database `olist`. Power BI needs **MySQL Connector/NET** installed.

The pipeline validates itself: `fact_orders` should hold 99,441 distinct orders and `fact_order_items` about 13.5M in total price.

## Design decisions and data notes
- **Staging then marts:** raw data is loaded unchanged into `stg_*` tables, and all business logic lives in one stored procedure, so the model can be rebuilt with a single `CALL sp_refresh_marts()`.
- **Item-level measures:** seller and category analysis uses measures based on `fact_order_items`, because filters from sellers and products do not flow up to the order-level table.
- **Customer identity:** `customer_unique_id` is used, not `customer_id`, since Olist issues a new `customer_id` per order.
- **Canceled orders** are excluded from item revenue. Segmentation uses delivered orders only, so its customer count is lower than the dashboard total.
- **Date range:** Olist volume is very small before 2017 and after Aug 2018, so year-over-year comparisons are meaningful only for Jan to Aug 2018 against the same months of 2017.
- **Geolocation data** is not used.

## Possible extensions
- Add a drill-through page for category detail.
- Add a payment-method analysis (the data is already in `fact_orders`).
- Schedule the pipeline and publish the report to the Power BI Service.
- Test additional cluster counts and compare silhouette scores.

## Author
**Lohith B N**: Data Analyst | Power BI Developer
[LinkedIn](https://www.linkedin.com/in/lohith-b-n) · [GitHub](https://github.com/Lohithbn12)

<!--
## Dashboard screenshots
Upload your PNGs to a `screenshots/` folder, delete the comment markers around this section, and use:
![Executive Overview](screenshots/page1_overview.png)
-->
