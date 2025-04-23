import pandas as pd
import os

data_folder = "data"
files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
dfs = []

for file in files:
    path = os.path.join(data_folder, file)
    df = pd.read_csv(path)

    df = df[df["product"] == "pink morsel"]
    
    df["price"] = df["price"].replace('[\$,]', '', regex=True).astype(float)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["sales"] = df["price"] * df["quantity"]
    
    df = df[["sales", "date", "region"]]

    dfs.append(df)

# Combine all into one DataFrame
final_df = pd.concat(dfs)

# Save to CSV
final_df.to_csv("formatted_sales_data.csv", index=False)

print("✅ Done! Output saved as 'formatted_sales_data.csv'")
