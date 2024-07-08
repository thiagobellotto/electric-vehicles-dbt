# Electric Vehicles Data Analysis

This project was built to demo an end-to-end project that will capture the analysis of electric vehicle trends across various model years and makes, specifically focusing on usage in Washington. It leverages modern data engineering practices and tools to provide interactive visualizations and insights.

## Technologies Used

- **dbt (Data Build Tool)**: Used for transforming raw data into insights using DuckDB.
- **DuckDB**: An embedded SQL database that acts as the data warehousing solution, perfect for analytical queries on the fly.
- **Streamlit**: For creating a dashboard that allow users to explore the data.
- **AWS S3**: Used for storing and retrieving dataset artifacts for accessible data storage.
- **GitHub Actions**: Used for the CI/CD pipeline for automated deployment of the data transformation and visualization components.

## Project Structure

```plaintext
.
├── .streamlit
│   └── config.toml         # Design definition for Streamlit
├── .github
│   └── workflows           # CI/CD workflows for GitHub Actions
├── dbt
│   └── models              # dbt project files (bronze -> golden layer)
├── streamlit_app           # Streamlit application code
├── Dockerfile-dbt          # Docker application for the dbt deployment
├── Dockerfile-s3          # Docker application for fetching and storing data
├── README.md
└── requirements.txt        # Python dependencies
```
