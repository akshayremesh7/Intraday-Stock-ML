import pandas as pd,glob,os

raw_path="data/raw"
clean_path="data/processed"

os.makedirs(clean_path,exist_ok=True)

files=glob.glob(os.path.join(raw_path,"*_yfinance.csv"))

for file in files:
    stock_name=os.path.basename(file).replace("_yfinance.csv","")
    print("cleaning",stock_name)
    df=pd.read_csv(file)
    
    new_cols = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume'] 
    df=pd.read_csv(file, skiprows=3, header=None, names=new_cols)
    date_cols=[c for c in df.columns if 'date' in c.lower()]
    # ... rest of the code
    if not date_cols:
        print(f"Skipping {stock_name}: No date column found")
        continue
    date_col=date_cols[0]
     
    df[date_col]=pd.to_datetime(df[date_col],errors='coerce')
    df=df.dropna(subset=[date_col])

    df=df.sort_values(by=date_col).reset_index(drop=True)

    df=df.fillna(method='ffill').fillna(method='bfill')

    df=df.drop_duplicates(subset=[date_col])

    df=df.rename(columns={date_col:'Date'})

    needed=['Date','Open','High','Low','Close','Adj Close','Volume']
    df=df[[c for c in needed if c in df.columns]]

    out=os.path.join(clean_path,f"{stock_name}_clean.csv")
    df.to_csv(out,index=False)
    print("Saved : ",out)

    print("Cleaning complete")