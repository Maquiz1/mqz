import pandas as pd
import os

# Step 1: Load the main .xlsx file
xls_path = '~/Documents/KEMR/DATA/TZ_Costing_Data_05_08_2025.xlsx'
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
    'ACCOM': 'Accompanying Person',
    'OOPYN': 'Pay Visit',
    'VDATE': 'Date',
    'VNO': 'Follow Up Number'
})

# Map facility codes to names
df_xls['Facility Code'] = df_xls['Facility Code'].map(facility_map).fillna(df_xls['Facility Code'])

# Pivot the DataFrame to get each follow-up in its own column
pivoted = df_xls.pivot_table(
    index=['Facility Code', 'PID'],
    columns='Follow Up Number',
    values=['Accompanying Person', 'Pay Visit', 'Date'],
    aggfunc='first'
)

# Flatten MultiIndex columns and rename for clarity
pivoted.columns = [
    f"Follow Up {col[1]} {'Date' if col[0]=='Date' else ('Accompanying Person' if col[0]=='Accompanying Person' else 'Pay Visit')}"
    for col in pivoted.columns
]
pivoted = pivoted.reset_index()

# Ensure all expected columns exist and in the requested order (Date, Accompanying Person, Pay Visit for each follow-up)
output_columns = ['Facility Code', 'PID']
for i in range(1, 5):
    output_columns.append(f'Follow Up {i} Date')
    output_columns.append(f'Follow Up {i} Accompanying Person')
    output_columns.append(f'Follow Up {i} Pay Visit')
    # Add missing columns if not present
    for col in [f'Follow Up {i} Date', f'Follow Up {i} Accompanying Person', f'Follow Up {i} Pay Visit']:
        if col not in pivoted.columns:
            pivoted[col] = None

pivoted = pivoted[output_columns]

print("Selected columns from merged data (with follow-up columns):")
print(pivoted.head())

pivoted.to_excel('~/Documents/KEMR/REPORTS/WP1/_2025_06_20_WP1_VL_DATA/WP1_TZ_COSTING_Data_06_20_2025.xlsx', index=False)
