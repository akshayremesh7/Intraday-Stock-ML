📈 Intraday Stock ML

A complete end-to-end intraday stock market machine learning pipeline built using Python.
This project covers data extraction → cleaning → feature engineering → model training → prediction → visualization, following a production-grade ML workflow.

🚀 Project Overview

This system predicts short-term intraday price movement direction using technical indicators such as:

EMA (8, 21, 50)

MACD (12, 26, 9)

RSI (14)

Bollinger Bands

ATR volatility

VWAP

Volume SMA / ratios

Rolling statistics

Lag features (previous bar info)

The project is structured like a real ML pipeline used in quantitative trading.

🧠 Key Features
✔ Data Extraction

Scripts inside src/extractors/ pull stock data and save them into:

data/raw/

✔ Data Cleaning

Cleans raw data by:

handling missing timestamps

forward/backward fill

sorting by date

removing duplicates

Outputs to:

data/processed/

✔ Feature Engineering

Inside src/features/
Creates technical indicators & engineered features:

EMA

MACD

RSI

Bollinger Bands

ATR

VWAP

Volume-based indicators

Rolling mean/std

Lag features

Saved to:

data/features/

✔ Model Training

Inside src/models/
Trains ML models like:

XGBoost

RandomForest

Includes:

train/validation/test split

performance metrics

saved predictions in data/predictions/

✔ Visualization

Inside src/visualize/
Generates:

price charts

technical indicator charts

predicted signals plots

📂 Project Folder Structure
Intraday-Stock-ML/
│
├── data/
│   ├── raw/            # Raw downloaded stock data
│   ├── processed/      # Cleaned data
│   ├── features/       # Technical indicator features
│   ├── predictions/    # Model predictions
│
├── src/
│   ├── extractors/     # Data extraction scripts
│   ├── preprocessors/  # Data cleaning logic
│   ├── features/       # Feature engineering
│   ├── models/         # Model training/evaluation
│   └── visualize/      # Visualization utilities
│
├── .gitignore
└── README.md

⚙️ Technology Stack

Python

Pandas / NumPy

TA-Lib (or custom indicator formulas)

Matplotlib / Seaborn

Scikit-Learn

XGBoost

YFinance / NSE API

📊 ML Task

A binary classification problem predicting if the next candle closes:

Up (1) → bullish

Down (0) → bearish

🧪 Evaluation Metrics

Accuracy

Precision

Recall

Confusion Matrix

(Optional) Profit-based evaluation

▶ How to Run
1️⃣ Extract raw data
python src/extractors/extract_data.py

2️⃣ Clean data
python src/preprocessors/clean_data.py

3️⃣ Build features
python src/features/build_features.py

4️⃣ Train model
python src/models/buildmodels.py

5️⃣ Visualize results
python src/visualize/visualisematlib.py

📌 Future Enhancements

Backtesting engine

LSTM / Temporal Convolution models

Streamlit dashboard

Live paper trading API

Ensemble models

🔥 Author

Akshay R
GitHub: akshayremesh7

Project Repo: Intraday-Stock-ML