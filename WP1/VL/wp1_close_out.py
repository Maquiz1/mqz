import pandas as pd
import os

# Step 1: Load the main .xlsx file
xls_path = '~/Documents/KEMR/DATA/TZ_Closeout_Data_06_16_2025.xlsx'
xls_path = os.path.expanduser(xls_path)
df_xls = pd.read_excel(xls_path, engine='openpyxl')

# Map FCODE values to facility names
facility_map = {
    1: 'Sinza',
    2: 'Mnazi mmoja',
    3: 'Amana',
    4: 'Mwananyamala'
}

# Rename columns for clarity
df_xls = df_xls.rename(columns={
    'FCODE': 'Facility Code',
    'ID': 'PID',
    'ASCLOS_DT': 'Close Date',
    'CLOS_RSN': 'Close Reason',
    'FORMCOMPDT': 'Date  Completed',
})

# Map facility codes to names
df_xls['Facility Code'] = df_xls['Facility Code'].map(facility_map).fillna(df_xls['Facility Code'])

# Select and reorder columns
output_columns = ['Facility Code', 'PID', 'Close Date', 'Close Reason', 'Date  Completed']
df_selected = df_xls[output_columns]

print("Selected columns from merged data (with follow-up columns):")
print(df_selected.head())

df_selected.to_excel('~/Documents/KEMR/REPORTS/WP1/_2025_06_20_WP1_VL_DATA/WP1_TZ_CLOSE_OUT_Data_06_20_2025.xlsx', index=False)
