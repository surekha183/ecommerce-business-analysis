# Olist E-commerce Delivery Performance Analytics Dashboard

## 📌 Project Overview

This project analyzes e-commerce delivery performance using the Olist Brazilian E-commerce dataset. The goal is to identify delivery delays, evaluate customer satisfaction, and understand differences in delivery performance across seller states and months.

The project uses **PostgreSQL, SQL, Power BI, and DAX** to transform raw data into meaningful business insights through an interactive dashboard.

## 🎯 Business Objectives

- Analyze overall order and delivery performance.
- Measure late delivery rates for eligible delivered orders.
- Compare customer review scores for late and on-time deliveries.
- Identify seller states with higher late delivery rates.
- Explore monthly delivery trends and performance patterns.
- Support data-driven decisions to improve delivery performance and customer satisfaction.

## 🛠️ Tools & Technologies

- **PostgreSQL** – Data storage, SQL queries, data validation, and views.
- **SQL** – Data analysis, joins, aggregations, and performance calculations.
- **Power BI** – Interactive dashboards, KPI cards, charts, and slicers.
- **DAX** – Calculated measures and delivery performance metrics.
- **GitHub** – Project documentation and version control.

## 📊 Key Performance Indicators

| Metric | Result |
|---|---:|
| Total Orders | 99,441 |
| Eligible Delivered Orders | 96,470 |
| Late Orders | 7,826 |
| Late Delivery Rate | 8.11% |
| Average Review Score — Late Deliveries | 2.57 |
| Average Review Score — On-time or Early Deliveries | 4.29 |

*Note: Delivery performance metrics are based on eligible delivered orders. Review scores are calculated from eligible delivery reviews. Results may vary when dashboard filters are applied.*

## 🔍 Key Insights

- **Delivery performance:** Approximately 8.11% of eligible delivered orders were classified as late.
- **Customer satisfaction:** Late deliveries had an average review score of 2.57, compared with 4.29 for on-time or early deliveries.
- **State-level analysis:** Seller-state comparisons help identify locations that may require further investigation into delivery performance.
- **Monthly trends:** Monthly analysis helps reveal changes in late delivery rates over time.
- **Customer feedback:** The dashboard compares low review rates for late deliveries and on-time or early deliveries.

## 📈 Dashboard Features

- KPI cards for total orders, eligible delivered orders, and late orders.
- Monthly late delivery rate analysis.
- Seller-state delivery performance comparison.
- Customer review score comparison by delivery result.
- Low customer review rate analysis.
- Interactive slicers and cross-filtering for exploring the data.

## 🗄️ Data Analysis Workflow

1. Obtained the Olist Brazilian E-commerce dataset.
2. Inspected and validated the source data.
3. Loaded the data into PostgreSQL.
4. Created SQL views for delivery performance and customer review analysis.
5. Calculated delivery metrics using SQL and DAX.
6. Connected PostgreSQL views to Power BI.
7. Developed interactive visuals and KPI cards.
8. Validated key metrics against SQL query results.

## 💡 Business Recommendations

- Investigate seller states with consistently high late delivery rates.
- Monitor monthly delivery performance to identify emerging problems.
- Review logistics and carrier performance to understand potential causes of delays.
- Track customer reviews alongside delivery outcomes.
- Use delivery performance metrics to prioritize operational improvements.

These recommendations identify areas for further investigation; the dashboard alone does not establish the causes of delivery delays.

## 📂 Project Structure

```text
olist-ecommerce-delivery-analytics/
│
├── sql/
│   ├── data_validation.sql
│   ├── delivery_performance.sql
│   └── analysis_views.sql
│
├── powerbi/
│   └── delivery_performance_dashboard.pbix
│
├── screenshots/
│   └── dashboard.png
│
└── README.md
```

*Update the file names and folders above to match your actual repository structure.*

## 🚀 How to Explore the Project

1. Clone or download this repository.
2. Import the Olist dataset into PostgreSQL.
3. Run the SQL scripts to create the required views.
4. Open the Power BI `.pbix` file.
5. Configure the PostgreSQL connection if prompted.
6. Use the dashboard slicers to explore delivery performance by month and seller state.

The original dataset is available on Kaggle: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

## 📚 Skills Demonstrated

SQL • PostgreSQL • Power BI • DAX • Data Validation • KPI Development • Data Visualization • Exploratory Data Analysis • Business Insights

## 👩‍💻 Author

**Vaitla Surekha**

Aspiring Data Analyst

[LinkedIn](https://www.linkedin.com/in/surekhavaitla/)

---

If you find this project useful, feel free to explore the repository and share your feedback.
