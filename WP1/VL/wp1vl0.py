import pandas as pd
import os

# Step 1: Load the main .xlsx file
xls_path = '~/Documents/KEMR/DATA/TZ_Eligibility_Data_06_16_2025.xlsx'
xls_path = os.path.expanduser(xls_path)
df_xls = pd.read_excel(xls_path, engine='openpyxl')

# Step 2: Load the enrollment data frame (adjust path and sheet name as needed)
enrollment_path = '~/Documents/KEMR/DATA/TZ_Enrollment_Data_06_16_2025.xlsx'  # <-- update this path if needed
enrollment_path = os.path.expanduser(enrollment_path)
df_enroll = pd.read_excel(enrollment_path, engine='openpyxl')

# Step 3: Merge the two dataframes on a common column (replace 'ID' with your actual key if needed)
merged_df = pd.merge(df_xls, df_enroll, on='ID', how='inner')

# Display only the first five columns of the first five rows
print("First five columns of merged data:")
# print(merged_df.iloc[:5, :5])

# Display specific columns: SCRID, VNO, VDATE (from eligibility) and VL (from enrollment)
columns_to_show = ['FCODE_x','SCRID', 'VNO_x', 'VDATE_x','VL', 'VLDATE','VLDATE','VL_VISIT','VDATE_y']  # Make sure these columns exist after merge
aliases = {
    'FCODE_x': 'Facility Code',
    'SCRID': 'Screening ID',
    'VNO_x': 'Visit Number',
    'VDATE_x': 'Eligibility Date',
        'VL': 'Eligibility Viral Load',
    'VLDATE': 'Eligibility Viral Load Date',
    'VL_VISIT': 'Enrollment Viral Load',
    'VDATE_y': 'Enrollment Date',
}

# Map FCODE_x values to facility names
facility_map = {
    1: 'Sinza',
    2: 'Mnazi mmoja',
    3: 'Amana',
    4: 'Mwananyamala'
}

selected = merged_df[columns_to_show].rename(columns=aliases)
selected['Facility Code'] = selected['Facility Code'].map(facility_map).fillna(selected['Facility Code'])

# Sort by FCODE_x and ID (use original merged_df columns for sorting)
# selected = selected.sort_values(by=['Facility Code', 'Screening ID'])


print("Selected columns from merged data (with aliases):")
print(selected.head())
selected.to_excel('~/Documents/KEMR/REPORTS/WP1/_2025_06_19_WP1_VL_DATA/WP1_VL_DATA_2025_06_19.xlsx', index=False)
