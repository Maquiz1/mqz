import pandas as pd

data = 'DATA/QUERIES/WP1/TZ_Eligibility_Data_06_16_2025.xls'
df = pd.read_excel(data)

# Optional: Display the first few rows
print(df.head())
