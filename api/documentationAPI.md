## CSV - API for Native Token Data / Ingest Data Feeds into Zipline and Backtrader Programs

As part of the Dataportal we like to provide a simple, free and lightweight API to allow users to download selected, cleaned Cardano native token time series data stored in the cloud. The first step is a minimal viable solution using open-source tools and a major cloud provider like AWS or Google with later optimization and redundancies possible.

This consists of initially four components:

1. Cloud Storage with AWS S3 or Google Cloud Storage to store our data.
2. API Framework: Python-based FastAPI that is easy to use and generates OpenAPI specs automatically
3. Cloud Hosting AWS Lambda or Google Cloud Functions to provide a serverless model
4. Client Script: Catalyst/Cardano users can execute simple Python script on their machine using the [requests](https://pypi.org/project/requests/) library

### Cloud Storage

### API Framework

### Cloud Hosting

### Client Script
