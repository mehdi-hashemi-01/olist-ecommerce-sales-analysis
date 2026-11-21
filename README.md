<div align="center">

# Olist E-Commerce Sales Analysis

**Sales, customer behavior, and delivery performance in Brazilian e-commerce**

![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.2+-150458?logo=pandas&logoColor=white)
[![Dataset](https://img.shields.io/badge/Dataset-Olist-087E8B)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
![Progress](https://img.shields.io/badge/Analysis-13_steps-25665B)

[Overview](#overview) · [Results](#results) · [Business recommendations](#business-recommendations) · [Dataset](#dataset) · [Script guide](#script-guide) · [Run locally](#run-locally)

</div>

## Overview

A sales manager sees a strong month on the dashboard. Did order volume rise, or did buyers spend more per order? This project uses Olist transactions to work through that question and two others. Which customers, cities, and categories account for the most sales? How often do deliveries miss their promised dates, and by how much?

Thirteen numbered scripts take the raw files from inspection to sales, customer and delivery results. Each script prints a short summary. Detailed results are available in CSV tables and seven figures.

## Results

| Business question | Result | Detail |
|:--|:--|:--|
| How much merchandise was sold? | **R$ 13,221,498.11** across **96,478 delivered orders**, averaging **R$ 137.04** per order. Freight totaled R$ 2,198,275.64. | [Sales KPIs](reports/tables/07_sales_kpis.csv) |
| Which purchase month led sales? | **November 2017**, with R$ 987,765.37 in merchandise sales. | [Monthly totals and growth](reports/tables/08_monthly_sales.csv) |
| How often did buyers return? | **2,801 of 93,358 buyers (3.00%)** placed at least two delivered orders within the observation window. | [Customer KPIs](reports/tables/10_customer_kpis.csv) |
| How often did deliveries miss the promise? | **6,534 of 96,470 evaluated orders (6.77%)** arrived after the promised calendar day. The other eight delivered orders lack an actual delivery timestamp. | [Delivery outcomes](reports/tables/05_delivery_outcomes.csv) |
| Which city and category led merchandise sales? | **São Paulo / SP** led cities with R$ 1,859,556.83. **Health & Beauty** led categories with R$ 1,233,131.72. | [Cities](reports/tables/11_city_sales.csv) · [Categories](reports/tables/12_category_sales.csv) |

### Order coverage and data quality

The nine source tables include **99,441 orders** and **112,650 order items**. Aggregating items by order ID before the join preserves all 99,441 order rows. Of those orders, 98,666 have item records and 775 have none. All 96,478 delivered orders have item values and together account for **110,197 items sold**. Sales are the sum of item prices in BRL. Freight is reported separately. [Table inventory](reports/tables/table_inventory.csv) · [Join checks](reports/tables/06_item_join_checks.csv) · [Sales KPIs](reports/tables/07_sales_kpis.csv)

All nonempty values in the five order timestamp columns parsed successfully. Of 2,965 orders missing a customer delivery timestamp, only **eight** have delivered status. Another six orders have canceled status and a recorded delivery date. The eight delivered orders count toward sales and are excluded from duration and punctuality calculations. The geolocation table contains 261,831 repeated full rows, and 58.70% of review records lack written comments. [Column profile](reports/tables/column_profile.csv) · [Date checks](reports/tables/02_date_checks.csv) · [Dates by status](reports/tables/03_dates_by_status.csv) · [14 flagged orders](reports/tables/03_delivery_exceptions.csv)

### Delivery speed and reliability

Customers received half of eligible orders within **10.22 days** of purchase and 90% within **23.10 days**. Of the 96,470 evaluated deliveries, 88,644 arrived early, 1,292 arrived on the promised calendar day and 6,534 arrived late. Among late orders alone, the median delay was **7 days** and the mean was **10.62 days**. Duration measures elapsed time since purchase. Lateness uses the difference between the actual and estimated calendar dates. [Duration percentiles](reports/tables/04_duration_stats.csv) · [Delivery outcomes](reports/tables/05_delivery_outcomes.csv) · [Delay among late orders](reports/tables/05_late_delay_stats.csv)

![Early, on-day and late deliveries as shares of 96,470 evaluated orders](assets/figures/05_compare_delivery_dates/delivery_outcomes.png)

### Why November 2017 sales grew

| Delivered orders by purchase month | October 2017 | November 2017 | Change |
|:--|--:|--:|--:|
| Merchandise sales | R$ 648,247.65 | R$ 987,765.37 | +52.37% |
| Orders | 4,478 | 7,289 | +62.77% |
| Average order value | R$ 144.76 | R$ 135.51 | −6.39% |
| Items per order | 1.1644 | 1.1627 | −0.14% |
| Average selling price per item | R$ 124.33 | R$ 116.55 | −6.26% |

The extra **2,811 orders** drove the highest sales month in the report. At October’s average order value, those additional orders would have added about R$ 406,928. The lower average value across November orders offset about R$ 67,410, leaving an observed gain of **R$ 339,517.72**. Basket size barely moved. Most of the fall in order value came from the lower price per item. Calculations use the underlying totals before rounding. [Monthly sales, order counts and growth](reports/tables/08_monthly_sales.csv)

![Monthly merchandise sales in BRL](assets/figures/09_plot_monthly_trends/total_sales.png)

| How many orders were placed? | How much merchandise did each order contain in BRL? |
|:--|:--|
| ![Delivered order count by purchase month](assets/figures/09_plot_monthly_trends/order_count.png) | ![Average merchandise value per delivered order](assets/figures/09_plot_monthly_trends/average_order_value.png) |

The charts show January 2017 through August 2018. The CSV includes every month between the first and last observed delivered purchases, including months with zero qualifying orders. Growth is blank when the preceding month is missing or has zero sales. Boundary months can have incomplete coverage.

### October and November 2017 by product

The mean selling price per delivered item fell from **R$ 124.33 to R$ 116.55**. Of 920 product IDs sold in both months, 156 had a lower mean price, 121 a higher one, and 643 the same. These counts weight every product equally. The decomposition below weights each product by units sold.

| Contribution to the overall change | BRL per item |
|:--|--:|
| Restrict October to products also sold in November | −10.55 |
| Change in selling prices among the matched products | −1.31 |
| Change in unit shares among the matched products | −10.79 |
| Expand November to include products sold only in November | +14.87 |
| **Total change** | **−7.78** |

The comparison moves from October's full basket to the October matched basket, then to the November matched basket, and finally to November's full basket. Average unit shares and prices across both months split the matched change symmetrically. The net product mix contribution was **−R$ 6.47 (83.2% of the overall fall)** under this method. A product observed in only one month has no observed price in the other month. Changes in observed selling prices can also reflect different sellers.

![Contributions to the fall in average item price](assets/figures/13_compare_product_prices/price_change.png)

### Customers, cities and product categories

**2,801 of 93,358 buyers** placed at least two delivered orders in the observation window. Buyers are counted using `customer_unique_id`. The highest-spending buyer spent **R$ 13,440 on one order**, illustrating why spend and repeat purchase are separate customer measures. Buyers who entered near the end of the dataset had less time to place another order. [Buyer KPIs](reports/tables/10_customer_kpis.csv) · [Top 10 buyers](reports/tables/10_top_customers.csv)

| City and state | Merchandise sales | Share of sales | Product category | Merchandise sales | Share of sales |
|:--|--:|--:|:--|--:|--:|
| São Paulo / SP | R$ 1,859,556.83 | 14.06% | Health & Beauty | R$ 1,233,131.72 | 9.33% |
| Rio de Janeiro / RJ | R$ 955,573.97 | 7.23% | Watches & Gifts | R$ 1,166,176.98 | 8.82% |
| Belo Horizonte / MG | R$ 346,039.04 | 2.62% | Bed, Bath & Table | R$ 1,023,434.76 | 7.74% |

São Paulo and Rio de Janeiro together accounted for **21.29% of merchandise sales**. Health & Beauty led categories by sales, while Bed, Bath & Table sold more units than either of the two categories above it. City totals use the buyer’s city and state. Category totals use each individual item’s category, so an order containing two categories can count toward both categories’ order counts. [Full city ranking](reports/tables/11_city_sales.csv) · [Full category ranking](reports/tables/12_category_sales.csv)

| Top cities by merchandise sales | Top categories by merchandise sales |
|:--|:--|
| ![Ten highest-selling city and state pairs](assets/figures/11_rank_cities/top_sales.png) | ![Ten highest-selling product categories](assets/figures/12_rank_product_categories/top_sales.png) |

## Business recommendations

| Evidence | Suggested action |
|:--|:--|
| November order volume rose 62.77% while average order value fell 6.39%. | Plan fulfillment capacity using projected orders and units. Track average order value separately when setting a sales target. |
| Product mix accounts for 83.2% of the observed fall in mean item price under the matched-product comparison. | Review the products gaining unit share before changing prices. Add product cost data before making margin decisions. |
| Late deliveries missed their promise by a median of seven days. | Break late deliveries down by route or seller, showing both late-order counts and rates, before choosing where to intervene. |
| The observed repeat-buyer rate was 3.00%. | Compare first-purchase cohorts over the same follow-up period before setting a retention target. |

## Dataset

The **Brazilian E-Commerce Public Dataset by Olist** contains anonymized orders placed on Brazilian marketplaces between 2016 and 2018. Olist provides nine CSV files. Each describes a different part of a purchase. [Dataset on Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) · [Download the CSV archive](https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce)

| Table | What one row describes | Use in this analysis |
|:--|:--|:--|
| Orders | One order | Status, purchase time, delivery date and promised date |
| Customers | One order-linked customer record | Join on `customer_id`, then track buyers across orders with `customer_unique_id` |
| Order items | One item within an order | Identify an item by `order_id` and `order_item_id`. Sum `price` for merchandise sales |
| Order payments | One payment entry within an order | Profile payment records and their completeness |
| Order reviews | One recorded review entry | Profile scores and missing review text |
| Products | One product | Map `product_id` to a category |
| Sellers | One seller | Profile seller records and identifiers |
| Geolocation | One location observation for a postal prefix | Audit duplicate location records and postal prefixes |
| Category translations | One category name and its English translation | Label product category charts |

### Relationships available in the source data

```mermaid
flowchart TD
    O["Orders"] -->|"customer_id"| C["Customers"]
    O -->|"order_id"| I["Order items"]
    O -->|"order_id"| P["Payments"]
    O -->|"order_id"| R["Reviews"]
    I -->|"product_id"| PR["Products"]
    I -->|"seller_id"| S["Sellers"]
    PR -->|"category name"| T["Category translations"]
    C -->|"postal prefix"| G["Geolocation grouped by prefix"]
    S -->|"postal prefix"| G
```

An order with two items and two payment entries produces four rows if both detail tables are joined directly on `order_id`. For order-level analysis, total each detail table separately before joining it to orders. Keep an item-level table for category rankings.

## Run locally

Use Python 3.11. Extract the nine source CSVs directly into `data/raw/`. Run the commands below from the repository root. The scripts also work from an IDE with the same Python environment.

```bash
python -m pip install -r requirements.txt
python scripts/01_inspect_data.py
```

Continue in the numbered order below. To reproduce all stages from a Windows PowerShell terminal:

```powershell
Get-ChildItem scripts/[0-9]*.py | Sort-Object Name | ForEach-Object {
    python $_.FullName
    if ($LASTEXITCODE -ne 0) { throw "Stage failed: $($_.Name)" }
}
```

## Script guide

| Script | What to learn | Input stage | Result to inspect |
|:--|:--|:--|:--|
| [01_inspect_data.py](scripts/01_inspect_data.py) | Read nine CSVs, count missing values and exact duplicates | Raw files | [Table inventory](reports/tables/table_inventory.csv) · [Column profile](reports/tables/column_profile.csv) |
| [02_check_order_dates.py](scripts/02_check_order_dates.py) | Check order keys and distinguish missing dates from parsing errors | Raw orders | [Date checks](reports/tables/02_date_checks.csv) |
| [03_check_delivery_records.py](scripts/03_check_delivery_records.py) | Group missing dates by status and flag contradictory records | 02 | [Status counts](reports/tables/03_dates_by_status.csv) · [Flagged orders](reports/tables/03_delivery_exceptions.csv) |
| [04_measure_delivery_times.py](scripts/04_measure_delivery_times.py) | Subtract timestamps and interpret the median and percentiles | 02 | [Duration statistics](reports/tables/04_duration_stats.csv) |
| [05_compare_delivery_dates.py](scripts/05_compare_delivery_dates.py) | Compare calendar days and calculate delay severity among late orders | 04 | [Outcomes](reports/tables/05_delivery_outcomes.csv) · [Late orders only](reports/tables/05_late_delay_stats.csv) |
| [06_build_order_totals.py](scripts/06_build_order_totals.py) | Check item keys, group items and join totals to orders | 02 + raw items | [Join checks](reports/tables/06_item_join_checks.csv) |
| [07_calculate_sales_kpis.py](scripts/07_calculate_sales_kpis.py) | Define the sales population and calculate average order value | 06 | [Sales KPIs](reports/tables/07_sales_kpis.csv) |
| [08_analyze_monthly_sales.py](scripts/08_analyze_monthly_sales.py) | Group by purchase month, fill missing months and calculate growth | 07 | [Monthly table](reports/tables/08_monthly_sales.csv) |
| [09_plot_monthly_trends.py](scripts/09_plot_monthly_trends.py) | Read a summary table and plot sales, order count and average order value | 08 | [Monthly charts](assets/figures/09_plot_monthly_trends/) |
| [10_analyze_repeat_customers.py](scripts/10_analyze_repeat_customers.py) | Join customers and count distinct orders per buyer | 07 + raw customers | [Buyer KPIs](reports/tables/10_customer_kpis.csv) · [Top 10 customers](reports/tables/10_top_customers.csv) |
| [11_rank_cities.py](scripts/11_rank_cities.py) | Rank city and state pairs by merchandise sales | 10 | [City sales](reports/tables/11_city_sales.csv) |
| [12_rank_product_categories.py](scripts/12_rank_product_categories.py) | Join products and translations to delivered items, then reconcile category sales | 07 + raw items, products and translations | [Category sales](reports/tables/12_category_sales.csv) |
| [13_compare_product_prices.py](scripts/13_compare_product_prices.py) | Match product IDs across two months and separate price from unit mix | Raw orders and items | [Product comparison](reports/tables/13_product_price_comparison.csv) · [Contributions](reports/tables/13_price_effects.csv) |

## Repository structure

| Folder | Contents |
|:--|:--|
| `data/raw/` | The nine original Olist CSVs, downloaded separately |
| `data/processed/` | Intermediate order, delivery and customer tables generated locally |
| `scripts/` | Thirteen numbered scripts. The two shared modules contain paths and chart formatting |
| `reports/tables/` | Small CSV reports. Files from steps 02–13 start with their step number |
| `assets/figures/` | Exported charts grouped by the script that produced them |

## Next step

Rank matched products by their contribution to the change in unit mix, then group contributions by category to identify where buying patterns shifted most.
