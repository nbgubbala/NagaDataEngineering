# NagaDataEngineering

A hands-on data engineering repository focused on learning, prototyping, and building real-world examples using modern data tools.

This project contains starter implementations for data pipelines, streaming concepts, PostgreSQL setup, Spark processing, and a small browser-based dashboard for visualizing sample data.

## Overview

The repository is organized around common data engineering building blocks:

- Databricks examples and configs
- Kafka producer/consumer examples
- PostgreSQL schema and migration structure
- PySpark data processing and local dashboard demo

## Repository structure

```text
NagaDataEngineering/
├── README.md
├── databricks/
│   ├── jobs/
│   ├── notebooks/
│   └── pipeline_config.json
├── kafka/
│   ├── configs/
│   ├── consumers/
│   ├── producers/
│   └── consumer_config.properties
├── postgresql/
│   ├── migrations/
│   ├── README.md
│   └── schema_init.sql
├── pyspark/
│   ├── app.py
│   ├── data_ui.html
│   ├── employees.csv
│   ├── sample_data.json
│   ├── test_data_example.py
│   └── configs/
└── .git/
```

## Current components

### Databricks
- Job and notebook starter folders
- Sample pipeline configuration

### Kafka
- Topic and consumer/producer configuration examples
- Environment setup for message-driven workflows

### PostgreSQL
- Schema initialization script
- Migration folder structure for SQL-based database setup

### PySpark
- Sample employee dataset in CSV format
- Spark script that reads CSV and generates JSON for the dashboard
- Simple Flask app and HTML UI for viewing the data in the browser

## Quick start

### PySpark dashboard

From the PySpark folder:

```powershell
cd C:\workspace\NagaDataEngineering\pyspark
python test_data_example.py
python app.py
```

Then open the app in a browser:

```text
http://127.0.0.1:5000
```

## Tech stack

- Python
- PySpark
- Flask
- PostgreSQL
- Kafka
- Databricks
- GitHub

## Learning goals

- Build reusable data engineering project structure
- Practice ingestion and transformation patterns
- Work with streaming and batch data concepts
- Explore schema design and database setup
- Create simple dashboards for data validation and visualization

## Status

This repository is currently in an active learning and prototype stage. The structure is intentionally simple and designed to expand as workflows and projects grow.

## Notes

The project is meant to be a practical learning repository and portfolio base for modern data engineering work. It is structured to support experimentation while staying easy to navigate and extend.
