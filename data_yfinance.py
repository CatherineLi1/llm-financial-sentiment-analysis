import yfinance as yf
import pandas as pd

ticks = ["XLF", # Large cap financial companies
         "VFH", # Mid/small cap financial companies
         "KBE", # Equal weight banks
] 

start = "2018-01-01"
end = "2018-05-31"
interval = "1d" # or "1wk"

for tick in ticks:
    df = yf.download(
        tick,
        start=start, # Inclusive
        end=end, # Exclusive
        interval=interval
    )
    df.columns = df.columns.droplevel(1)
    df = df.reset_index()
    df.to_csv(f"data/tickers/{tick}_{start}_{end}_{interval}.csv", index=False)


