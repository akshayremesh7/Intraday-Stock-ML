import pandas as pd

import numpy as np

import os

from datetime import date, timedelta

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

from sklearn.metrics import r2_score, accuracy_score



# Paths

features_path = "data/features"

output_path = "data/predictions"

os.makedirs(output_path, exist_ok=True)



# === DYNAMIC DATE RANGE ===

today = date.today()

start_date = (today - timedelta(days=2*365)).strftime("%Y-%m-%d")

end_date = today.strftime("%Y-%m-%d")

print(f"📅 Using data from {start_date} to {end_date}")



# Detect feature files

stocks = [f.replace("_features.csv", "") for f in os.listdir(features_path) if f.endswith("_features.csv")]



def process_stock(stock_name):

    file_path = os.path.join(features_path, f"{stock_name}_features.csv")

    if not os.path.exists(file_path):

        print(f"⚠️ Skipping {stock_name}: file not found.")

        return None



    print(f"\n🔹 Processing {stock_name} ...")



    df = pd.read_csv(file_path)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    df = df.dropna().reset_index(drop=True)



    # ✅ Filter only recent 2 years of data

    df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]



    if len(df) < 100:

        print(f"⚠️ Not enough recent data for {stock_name}. Skipping...")

        return None



    # Target creation

    df["Next_Close"] = df["Close"].shift(-1)

    df = df.dropna()

    df["Price_Change"] = df["Next_Close"] - df["Close"]

    df["Price_Direction"] = np.where(df["Price_Change"] > 0.5, 1,

                              np.where(df["Price_Change"] < -0.5, -1, 0))



    # Auto-detect features

    exclude = ["Date", "Next_Close", "Price_Change", "Price_Direction"]

    features = [col for col in df.columns if col not in exclude and np.issubdtype(df[col].dtype, np.number)]



    if len(features) < 5:

        print(f"⚠️ Not enough numeric features for {stock_name}. Skipping...")

        return None



    X = df[features]

    y_reg = df["Next_Close"]

    y_clf = df["Price_Direction"]



    X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test = train_test_split(

        X, y_reg, y_clf, test_size=0.2, shuffle=False

    )



    # Time-based weighting (recent samples more important)

    weights = np.linspace(0.1, 1, len(X_train))



    # Train models

    reg_model = RandomForestRegressor(n_estimators=250, max_depth=10, random_state=42)

    clf_model = RandomForestClassifier(n_estimators=350, max_depth=10, random_state=42)



    reg_model.fit(X_train, y_reg_train, sample_weight=weights)

    clf_model.fit(X_train, y_clf_train, sample_weight=weights)



    # Predictions

    y_reg_pred = reg_model.predict(X_test)

    y_clf_pred = clf_model.predict(X_test)



    # Metrics

    r2 = r2_score(y_reg_test, y_reg_pred)

    accuracy = accuracy_score(y_clf_test, y_clf_pred)



    # Recent accuracy (last 25% of test data)

    n_recent = int(len(y_clf_test) * 0.25)

    y_recent_true = y_clf_test[-n_recent:]

    y_recent_pred = y_clf_pred[-n_recent:]

    recent_acc = accuracy_score(y_recent_true, y_recent_pred)



    # Latest prediction

    latest_data = X.iloc[-1:].values

    predicted_price = reg_model.predict(latest_data)[0]

    predicted_signal = clf_model.predict(latest_data)[0]



    signal = "BUY" if predicted_signal == 1 else "SELL" if predicted_signal == -1 else "HOLD"



    print(f"✅ {stock_name}: Predicted Price ₹{predicted_price:.2f} | Signal: {signal}")

    print(f"📊 Accuracy: {accuracy*100:.2f}% | Recent Accuracy: {recent_acc*100:.2f}%")



    return {

        "Stock": stock_name,

        "Predicted_Price": round(predicted_price, 2),

        "Signal": signal,

        "R2_Score": round(r2, 3),

        "Accuracy": round(accuracy * 100, 2),

        

        "Data_End": end_date

    }



# Run for all stocks

results = []

for stock in stocks:

    res = process_stock(stock)

    if res:

        results.append(res)



if results:

    report_df = pd.DataFrame(results)

    output_file = os.path.join(output_path, "daily_signals.csv")

    report_df.to_csv(output_file, index=False)

    print("\n✅ All Stocks Processed Successfully!")

    print(report_df)

else:

    print("\n⚠️ No stocks processed successfully.")
    