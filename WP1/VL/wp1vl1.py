import pandas as pd
import os

# Step 1: Load the main .xlsx file
xls_path = '~/Documents/KEMR/DATA/TZ_FollowUp_Data_06_16_2025.xlsx'
xls_path = os.path.expanduser(xls_path)
df_xls = pd.read_excel(xls_path, engine='openpyxl')

# Map FCODE values to facility names
facility_map = {
    1: 'Sinza',
    2: 'Mnazi mmoja',
    3: 'Amana',
    4: 'Mwananyamala'
}

# Prepare output DataFrame with unique IDs and facility codes
output_columns = [
    'Facility Code', 'PID',
    'Follow Up 1 Viral Load', 'Follow Up 1 Date',
    'Follow Up 2 Viral Load', 'Follow Up 2 Date',
    'Follow Up 3 Viral Load', 'Follow Up 3 Date',
    'Follow Up 4 Viral Load', 'Follow Up 4 Date'
]

# Rename columns for clarity
df_xls = df_xls.rename(columns={
    'FCODE': 'Facility Code',
    'ID': 'PID',
    'VL_VISIT': 'Viral Load',
    'VDATE': 'Date',
    'VNO': 'Follow Up Number'
})

# Map facility codes to names
df_xls['Facility Code'] = df_xls['Facility Code'].map(facility_map).fillna(df_xls['Facility Code'])

# Pivot the DataFrame to get each follow-up in its own column
pivoted = df_xls.pivot_table(
    index=['Facility Code', 'PID'],
    columns='Follow Up Number',
    values=['Viral Load', 'Date'],
    aggfunc='first'
)

# Flatten MultiIndex columns and rename for clarity
pivoted.columns = [
    f"Follow Up {col[1]} {'Viral Load' if col[0]=='Viral Load' else 'Date'}"
    for col in pivoted.columns
]
pivoted = pivoted.reset_index()

# Ensure all expected columns exist
for i in range(1, 5):
    for suffix in ['Viral Load', 'Date']:
        col = f'Follow Up {i} {suffix}'
        if col not in pivoted.columns:
            pivoted[col] = None

# Reorder columns
pivoted = pivoted[output_columns]

print("Selected columns from merged data (with follow-up columns):")
print(pivoted.head())

pivoted.to_excel('~/Documents/KEMR/REPORTS/WP1/_2025_06_19_WP1_VL_DATA/WP1_TZ_FollowUp_Data_06_19_2025.xlsx', index=False)
