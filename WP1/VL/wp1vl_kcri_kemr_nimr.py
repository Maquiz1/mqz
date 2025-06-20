import pandas as pd
import os

# --- Load REDCap V4 and V6 data ---
csv_path_v4 = '~/Documents/KEMR/REDCAP_DATA/V4/ALL/EAPOC_DATA_2025-02-05_1149.csv'
csv_v4 = os.path.expanduser(csv_path_v4)
df_v4 = pd.read_csv(csv_v4)

csv_path_v6 = '~/Documents/KEMR/REDCAP_DATA/V6/ALL/EAPOCV60_DATA_2025-02-07_1154.csv'
csv_v6 = os.path.expanduser(csv_path_v6)
df_v6 = pd.read_csv(csv_v6)

facilities = [
    'mnazi_mmoja_hospit',
    'amana_hospital',
    'sinza_hospital',
    'mwananyamala_hospi'
]
df_v4 = df_v4[df_v4['redcap_data_access_group'].isin(facilities)]
df_v6 = df_v6[df_v6['redcap_data_access_group'].isin(facilities)]

v4eligibility = df_v4[df_v4['redcap_event_name'] == 'screening_arm_1'][
    ['record_id', 'redcap_event_name', 'redcap_data_access_group', 'd_visit_date']
]
v4enrollment = df_v4[df_v4['redcap_event_name'] == 'enrollment_v1_arm_1'][
    ['record_id', 'redcap_event_name', 'redcap_data_access_group', 'visit_date', 'when_was_the_sample_for_th']
]
v6followup = df_v6[df_v6['redcap_event_name'] == 'month_6_v2_arm_1'][
    ['record_id', 'redcap_event_name', 'redcap_data_access_group', 'what_is_the_viral_load_res2', 'a_when_was_the_sample_for2']
]

v4eligibility['record_id'] = v4eligibility['record_id'].astype(str)
v4enrollment['record_id'] = v4enrollment['record_id'].astype(str)
v6followup['record_id'] = v6followup['record_id'].astype(str)

v4_merged = pd.merge(
    v4eligibility,
    v4enrollment,
    on='record_id',
    how='inner',
    suffixes=('_elig', '_enroll')
)

final_merged = pd.merge(
    v4_merged,
    v6followup,
    on='record_id',
    how='inner',
    suffixes=('', '_followup')
)

final_merged['Facility'] = final_merged['redcap_data_access_group_elig'].combine_first(
    final_merged['redcap_data_access_group_enroll']
).combine_first(
    final_merged['redcap_data_access_group']
)

final_selected = final_merged[
    [
        'Facility',
        'record_id',
        'd_visit_date',
        'when_was_the_sample_for_th',
        'visit_date',
        'what_is_the_viral_load_res2',
        'a_when_was_the_sample_for2'
    ]
]

final_selected = final_selected.rename(columns={
    'record_id': 'PID',
    'd_visit_date': 'Eligibility Date',
    'when_was_the_sample_for_th': 'Eligibility Viral Load Date',
    'visit_date': 'Enrollment Date',
    'what_is_the_viral_load_res2': 'Followup 1 Viral Load',
    'a_when_was_the_sample_for2': 'Followup 1 Date',
})

# --- Load v12 followup data ---
xlsx_path_v12 = '~/Documents/KEMR/DATA/TZ_FollowUp_Data_06_16_2025.xlsx'
xlsx_v12 = os.path.expanduser(xlsx_path_v12)
df_v12 = pd.read_excel(xlsx_v12)
v12followup = df_v12[df_v12['VNO'] == 2][['ID', 'VDATE', 'VL_VISIT']]
v12followup['ID'] = v12followup['ID'].astype(str)

final_selected['PID'] = final_selected['PID'].astype(str)
final_merged_with_v12 = pd.merge(
    final_selected,
    v12followup,
    left_on='PID',
    right_on='ID',
    how='left'
).drop(columns=['ID'])

final_merged_with_v12 = final_merged_with_v12.rename(columns={
    'VL_VISIT': 'Followup 2 Viral Load',
    'VDATE': 'Followup 2 Viral Load Date',
})

# --- Load client data from wp1vl_nimr_clients.py ---
csv_client_path = '~/Documents/KEMR/DATA_NIMR/clients_2025_0619.csv'
client_path = os.path.expanduser(csv_client_path)
df_client = pd.read_csv(client_path)

# Filter clients where status == 1
df_client = df_client[df_client['status'] == 1]

# Map site_id to facility names
site_map = {
    1: 'Sinza Hospital',
    2: 'Mnazi mmoja hospital',
    3: 'Amana hospital',
    4: 'Mwananyamala Hospital'
}
df_client['facility'] = df_client['site_id'].map(site_map)

# Fix enrollment_id values as requested
df_client['enrollment_id'] = df_client['enrollment_id'].replace({
    3333022: 333022,
    33109: 331009
})

# Only take these columns from clients
client_columns = ['facility', 'id', 'enrollment_id', 'vl', 'vl_date', 'recent_vl', 'recent_vl_date']
df_client = df_client[client_columns]


# Remove decimal points from enrollment_id (convert to int then str)
df_client['enrollment_id'] = df_client['enrollment_id'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else '')

# Make sure both columns are string for merging
final_merged_with_v12['PID'] = final_merged_with_v12['PID'].astype(str)
df_client['enrollment_id'] = df_client['enrollment_id'].astype(str)

# Merge final_merged_with_v12 with df_client using PID <-> enrollment_id
final_merged_with_clients = pd.merge(
    final_merged_with_v12,
    df_client,
    left_on='PID',
    right_on='enrollment_id',
    how='left',
    suffixes=('', '_client')
)

# Drop unwanted columns from the final data set
final_merged_with_clients = final_merged_with_clients.drop(
    columns=['facility', 'id', 'enrollment_id', 'vl_date', 'recent_vl_date'],
    errors='ignore'
)


# Reorder columns: recent_vl after Eligibility Date, vl before Enrollment Date
cols = list(final_merged_with_clients.columns)
# Remove if already present
for col in ['recent_vl', 'vl']:
    if col in cols:
        cols.remove(col)
# Insert recent_vl after Eligibility Date
elig_idx = cols.index('Eligibility Date')
cols.insert(elig_idx + 1, 'recent_vl')
# Insert vl before Enrollment Date
enroll_idx = cols.index('Enrollment Date')
cols.insert(enroll_idx, 'vl')
final_merged_with_clients = final_merged_with_clients[cols]


# Rename recent_vl and vl columns
final_merged_with_clients = final_merged_with_clients.rename(columns={
    'recent_vl': 'Eligibility Viral Load',
    'vl': 'Enrollment Viral Load'
})


# Function to highlight empty columns in red
def highlight_empty_columns(s):
    is_empty = s.isnull() | (s == '')
    return ['background-color: red' if is_empty.all() else '' for _ in s]

# Apply the highlighting to columns that are completely empty
styled = final_merged_with_clients.style.apply(highlight_empty_columns, axis=0)


print("Final merged with client data (first 5 rows):")
print(final_merged_with_clients.head())

# Optionally save the merged result
# final_merged_with_clients.to_excel(
#     '~/Documents/KEMR/REPORTS/WP1/_2025_06_20_WP1_VL_DATA/WP1_VL_NIMR_DATASETS_FINAL_2025_06_20.xlsx',
#     index=False
# )

# Optionally save the merged result as Excel with red highlights for empty columns
output_path = '~/Documents/KEMR/REPORTS/WP1/_2025_06_20_WP1_VL_DATA/WP1_VL_NIMR_DATASETS_FINAL_2025_06_20.xlsx'
output_path = os.path.expanduser(output_path)
styled.to_excel(output_path, index=False, engine='openpyxl')
