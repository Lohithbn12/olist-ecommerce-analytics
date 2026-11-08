# Power BI Desktop steps
1. Get Data > MySQL database > Server `localhost`, Database `olist` > Import.
   (Install MySQL Connector/NET first.) Load: fact_orders, fact_order_items,
   dim_product, dim_seller, dim_customer, customer_segments.
2. Power Query: check order_date is Date; delivery_days/delay_days are Whole Number.
3. Modeling > New table: paste `dim_date` from measures.dax; mark as date table.
4. Relationships (one-to-many, single direction):
   - dim_date[Date] -> fact_orders[order_date]
   - dim_customer[customer_unique_id] -> fact_orders[customer_unique_id]
   - dim_customer[customer_unique_id] -> customer_segments[customer_unique_id] (1:1)
   - fact_orders[order_id] -> fact_order_items[order_id]
   - dim_product[product_id] -> fact_order_items[product_id]
   - dim_seller[seller_id] -> fact_order_items[seller_id]
5. Enter Data > create empty table `_Measures`; paste all measures from measures.dax.
6. Build 4 pages:
   - Executive Overview: cards (Revenue, Orders, AOV, YoY %), line chart revenue by YearMonth + Revenue LY, filled map by state, year/quarter slicers
   - Products & Sellers: top 10 categories bar, revenue vs freight scatter, top 10 sellers table, treemap, drill-through to category page
   - Customers: segment donut, RFM table, Repeat Customer % card, customers by state, segment slicer
   - Delivery & Satisfaction: On-Time % gauge, avg delivery days by state, Avg Review Score by Delay Bucket, decomposition tree
7. Polish: theme, bookmark navigation buttons, tooltips, red conditional formatting for late deliveries, reset-filters button.
8. Save as powerbi/olist_dashboard.pbix and take screenshots into /screenshots.
