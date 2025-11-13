import numpy as np
import pandas as pd,glob,os

clean_path="data/processed"
features_path="data/features"

os.makedirs(features_path,exist_ok=True)

files=glob.glob(os.path.join(clean_path,"*_clean.csv"))

for file in files:
    stock=os.path.basename(file).replace("_clean.csv","")
    print(f"Building features for {stock}...")

    df=pd.read_csv(file)

    df["SMA10"]=df["Close"].rolling(window=10).mean()
    df["SMA20"]=df["Close"].rolling(window=20).mean()

    df["EMA10"]=df["Close"].ewm(span=10,adjust=False).mean()
    df["EMA20"]=df["Close"].ewm(span=20,adjust=False).mean()

    delta=df["Close"].diff()
    gain=np.where(delta>0,delta,0)
    loss=np.where(delta<0,-delta,0)
    avg_gain=pd.Series(gain).rolling(window=14).mean()
    avg_loss=pd.Series(loss).rolling(window=14).mean()
    rs=avg_gain/avg_loss
    df["RSI14"]=100-(100/(1+rs))

    ema12=df["Close"].ewm(span=12,adjust=False).mean()
    ema26=df["Close"].ewm(span=26,adjust=False).mean()
    df["MACD"]=ema12-ema26
    df["signal_line"]=df["MACD"].ewm(span=9,adjust=False).mean()

    df["BB_MIDDLE"]=df["Close"].rolling(window=20).mean()
    df["BB_UPPER"]=df["BB_MIDDLE"]+(df["Close"].rolling(window=20).std()*2)
    df["BB_LOWER"]=df["BB_MIDDLE"]-(df["Close"].rolling(window=20).std()*2)

    df["DAILY_RETURN"]=df["Close"].pct_change()
    df["VOLATILITY"]=df["DAILY_RETURN"].rolling(window=10).std()

    df.dropna(inplace=True)

    out=os.path.join(features_path,f"{stock}_features.csv")
    df.to_csv(out,index=False)
    
    print(f"✅ Saved: {out}")

    print("✅ All feature files created successfully.")