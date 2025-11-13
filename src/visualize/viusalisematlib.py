import pandas as pd
import glob,os
import matplotlib.pyplot as plt

features_path="data/features"


files=glob.glob(os.path.join(features_path,"*_features.csv"))

for file in files:
    stock=os.path.basename(file).replace("_features.csv"," ")
    print(f"Analysing features for {stock}...")

    df=pd.read_csv(file)

    df["Date"]=pd.to_datetime(df["Date"])
    print("Data loaded successfully")
    print(df.head())

    plt.figure(figsize=(12,6))
    plt.plot(df["Date"],df["Close"],label="Close Price",color="blue")
    plt.title('Stock Closing Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.pause(1)
  

    plt.figure(figsize=(12,6))
    plt.plot(df["Date"],df['Close'],label='Close',alpha=0.7)
    plt.plot(df["Date"],df["SMA10"],label='SMA10',color='orange')
    plt.plot(df["Date"], df["SMA20"], label="SMA20", color="green")
    plt.title("Simple moving average 10 & 20 days")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.pause(1)


    plt.figure(figsize=(12,4))
    plt.plot(df['Date'], df['RSI14'], color='purple')
    plt.axhline(70, color='red', linestyle='--', label='Overbought')
    plt.axhline(30, color='green', linestyle='--', label='Oversold')
    plt.title('RSI (Relative Strength Index)')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.pause(1)
 

    df = df.dropna(subset=['MACD', 'signal_line', 'BB_UPPER', 'BB_LOWER'])

    plt.figure(figsize=(12,5))
    plt.plot(df['Date'], df['MACD'], label='MACD', color='blue')
    plt.plot(df['Date'], df['signal_line'], label='Signal Line', color='orange')
    plt.title('MACD vs Signal Line')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.pause(1)

    plt.figure(figsize=(12,6))
    plt.plot(df['Date'], df['Close'], label='Close', color='blue')
    plt.plot(df['Date'], df['BB_MIDDLE'], label='Middle Band', color='black')
    plt.plot(df['Date'], df['BB_UPPER'], label='Upper Band', color='red')
    plt.plot(df['Date'], df['BB_LOWER'], label='Lower Band', color='green')
    plt.fill_between(df['Date'], df['BB_LOWER'], df['BB_UPPER'], alpha=0.1, color='grey')
    plt.title('Bollinger Bands')
    plt.legend()
    plt.grid(True)
    plt.show()