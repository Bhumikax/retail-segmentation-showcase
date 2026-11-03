# Retail Customer Segmentation

An interactive Streamlit showcase exploring customer purchasing behaviour through RFM (Recency, Frequency, Monetary) analysis and K-Means clustering.

## Project Overview

This project analyses historical transactions from the UCI Online Retail dataset to identify distinct customer purchasing patterns.

The showcase presents data preparation, customer segments, clustering evaluation, and sensitivity analysis.

## Methodology

- Data cleaning and preprocessing
- RFM feature engineering
- StandardScaler feature scaling
- K-Means clustering (k=4)
- Cluster profiling and evaluation
- Preprocessing sensitivity analysis

## Dataset

Source: [UCI Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)

The dataset contains historical transactions from a UK-based online retailer between 2010 and 2011.

Only aggregate analysis reports are included in this repository. Raw transaction data and customer-level RFM records are excluded.

## Run Locally

```bash
pip install -r requirements.txt
python -m streamlit run demo/app.py
```

## Important Note
The segments are exploratory behavioural groupings, not definitive customer classifications. Results depend on preprocessing and modelling choices, and smaller clusters may be less stable.

This project is intended for analytical demonstration and educational purposes.