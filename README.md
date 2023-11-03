# Cryptocurrency Mining Performance Dashboard

## Objective
Create a comprehensive dashboard that provides real-time insights into cryptocurrency mining operations using the f2pool's APIs (secondary data).

## Data Sources
- [f2pool API](https://www.f2pool.com/api_doc): Use the f2pool API to fetch data regarding mining performance.
- External APIs:
  1. [Mining difficulty level](https://academy.braiins.com/en/mining-insights/public-api/) - requires alternative API sources
  2. Forex rates for any given date (planned for future implementation - pffi).

## Rate Limits and Data overall Limitations 
- **braiins**: A maximum of 500 requests per hour and 2,000 per day. Granularity issue: cannot pull prices at 10 min granularity.

## Datasets
Planned for future implementation: Incorporate additional data, such as BTC market prices, for a more comprehensive analysis.

## Data Pipeline
- **Extract**: Retrieve data on mining hashrate performance, transaction history, relative BTC price, and difficulty levels from the specified API endpoints.
- **Transform**: Cleanse and aggregate data to calculate essential metrics such as revenue, average hashrate, stale rate, etc. Integrate data from various sources for a complete overview.
- **Load**: Transition the transformed data into an SQLite database. This stage also includes further data extraction, incorporating BTC price and Difficulty level data from the **braiins** API
![Loading Diff Price](/assets/loading_diff_price.png)
- **Import to Power BI**: Since Power BI does not support SQLite natively and the typical ODBC driver connection was not an option in my environment, an alternative approach was required to convert the `mining_data.db` to an Excel file for use.

## End Outcome
### Dashboard
Underestimated the effort required to use Power BI versus the time available. Tasks that initially seemed simple, such as converting Unix timestamps to a human-readable format or calculating revenue from the hashrate, required extensive data cleaning and additional transformations in Power Query.
![Current state](/assets/dashboard.png)

**Learning takeaways:**
- **Visualization**: The Drill Down Timeline PRO is an effective tool for timeline visualization.
- **Non-Standard Time Periods/Independent Hierarchies**: Timeline granularity is crucial in my case (needing to zoom in to 10-minute intervals), where the default Power BI date hierarchy is inadequate. Understanding how to work with non-standard time periods and creating independent hierarchies are significant learning points. 

The final dashboard should provide:
- Current balance and total payments (pffi)
- Mining performance metrics (current hashrate - pffi, average hashrate, rejected hashrate, etc.).
- Transaction history with filtering options (pffi).
- Distribution details for hashrate and revenue.
- Allow users to drill down into specific metrics for a detailed view.

## Additional Steps (pffi)
- **Scheduling**: Use Apache Airflow to regularly run the data pipeline, ensuring that the dashboard displays up-to-date information.
- **Version Control**: Maintain a GitHub repository for the project, ensuring that code changes are committed regularly with meaningful commit messages.

## Stretch Goals
- **Predictive Analytics**: Use the historical mining performance data to predict future earnings or hashrate performance.
- **Alerts**: Implement a system that notifies the user when certain metrics (like hashrate dropping below a threshold) are triggered.
- **Integration with Other Platforms**: Consider integrating with other mining platforms or financial tools to provide a unified view of the user's cryptocurrency operations.
