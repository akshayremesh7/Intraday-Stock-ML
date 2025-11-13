import yfinance as yf
from nsepython import nsefetch
from datetime import date
import requests
import pandas as pd
import time
import os 

os.makedirs("data/raw",exist_ok=True)

stocks=["TCS","INFY","RELIANCE","SBIN","HDFCBANK","ICICIBANK","AXISBANK","LT","KOTAKBANK","BHARTIARTL"]
start_date="2024-01-01"
end_date="2024-12-31"

for stock in stocks:
    print(f"Downloading {stocks} from yfinance...")
    data=yf.download(f"{stock}.NS",start=start_date,end=end_date)
    data.to_csv(f"data/raw/{stock}_yfinance.csv")
    print(f"Saved yfinance data for {stock}")

   
    