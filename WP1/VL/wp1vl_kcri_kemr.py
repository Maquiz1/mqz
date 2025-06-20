import pandas as pd
import os

# Step 1: Load the main .csv files
csv_path_v4 = '~/Documents/KEMR/REDCAP_DATA/V4/ALL/EAPOC_DATA_2025-02-05_1149.csv'
csv_v4 = os.path.expanduser(csv_path_v4)
df_v4 = pd.read_csv(csv_v4)

csv_path_v6 = '~/Documents/KEMR/REDCAP_DATA/V6/ALL/EAPOCV60_DATA_2025-02-07_1154.csv'
csv_v6 = os.path.expanduser(csv_path_v6)
df_v6 = pd.read_csv(csv_v6)

# Filter for specific facilities in both dataframes
facilities = [
    'mnazi_mmoja_hospit',
    'amana_hospital',
    'sinza_hospital',
    'mwananyamala_hospi'
]
df_v4 = df_v4[df_v4['redcap_data_access_group'].isin(facilities)]
df_v6 = df_v6[df_v6['redcap_data_access_group'].isin(facilities)]

# Create filtered DataFrames for each event and select only required columns
v4eligibility = df_v4[df_v4['redcap_event_name'] == 'screening_arm_1'][
    ['record_id', 'redcap_event_name', 'redcap_data_access_group', 'd_visit_date']
]
v4enrollment = df_v4[df_v4['redcap_event_name'] == 'enrollment_v1_arm_1'][
    ['record_id', 'redcap_event_name', 'redcap_data_access_group', 'visit_date', 'when_was_the_sample_for_th']
]
v6followup = df_v6[df_v6['redcap_event_name'] == 'month_6_v2_arm_1'][
    ['record_id', 'redcap_event_name', 'redcap_data_access_group', 'what_is_the_viral_load_res2', 'a_when_was_the_sample_for2']
]

# Ensure all record_id columns are string for merging
v4eligibility['record_id'] = v4eligibility['record_id'].astype(str)
v4enrollment['record_id'] = v4enrollment['record_id'].astype(str)
v6followup['record_id'] = v6followup['record_id'].astype(str)

# Merge v4eligibility and v4enrollment on 'record_id'
v4_merged = pd.merge(
    v4eligibility,
    v4enrollment,
    on='record_id',
    how='inner',
    suffixes=('_elig', '_enroll')
)

# Merge the above result with v6followup on 'record_id'
final_merged = pd.merge(
    v4_merged,
    v6followup,
    on='record_id',
    how='inner',
    suffixes=('', '_followup')
)

# Create a single 'Facility' column by prioritizing Eligibility, then Enrollment, then Followup Facility
final_merged['Facility'] = final_merged['redcap_data_access_group_elig'].combine_first(
    final_merged['redcap_data_access_group_enroll']
).combine_first(
    final_merged['redcap_data_access_group']
)

# Keep only the requested columns in the final data, with 'Facility' as the first column
final_selected = final_merged[
    [
        'Facility',
        'record_id',
        'd_visit_date',
        # 'what_is_the_most_recent_vi',
        'when_was_the_sample_for_th',
        'visit_date',
        'what_is_the_viral_load_res2',
        'a_when_was_the_sample_for2'
    ]
]

# Add aliases for final columns
final_selected = final_selected.rename(columns={
    'record_id': 'PID',
    'd_visit_date': 'Eligibility Date',
    # 'what_is_the_most_recent_vi': 'Eligibility Viral Load',
    'when_was_the_sample_for_th': 'Eligibility Viral Load Date',
    'visit_date': 'Enrollment Date',
    'what_is_the_viral_load_res2': 'Followup 1 Viral Load',
    'a_when_was_the_sample_for2': 'Followup 1 Date',
})

print("Final selected data (first 5 rows):")
print(final_selected.head())

# Optionally save the merged result
final_selected.to_excel('~/Documents/KEMR/REPORTS/WP1/REDCAP/_2025_06_19_WP1_VL_DATA/WP1_VL_NIMRDATA_FINAL_2025_06_19.xlsx', index=False)








xlsx_path_v12 = '~/Documents/KEMR/DATA/TZ_FollowUp_Data_06_16_2025.xlsx'
xlsx_v12 = os.path.expanduser(xlsx_path_v12)
df_v12 = pd.read_excel(xlsx_v12)

# Load new dataframe from v12 where VNO=2 and display columns ID, VDATE, VL_VISIT
v12followup = df_v12[df_v12['VNO'] == 2][['ID', 'VDATE', 'VL_VISIT']]
v12followup['ID'] = v12followup['ID'].astype(str)

print("v12followup (VNO=2) first 5 rows:")
print(v12followup.head())

# Optionally, merge v12followup with final_selected using PID <-> ID
final_selected['PID'] = final_selected['PID'].astype(str)
final_merged_with_v12 = pd.merge(
    final_selected,
    v12followup,
    left_on='PID',
    right_on='ID',
    how='left'
)

# Drop 'ID' column after merge if not needed
final_merged_with_v12 = final_merged_with_v12.drop(columns=['ID'])


# Add aliases for final columns
final_merged_with_v12 = final_merged_with_v12.rename(columns={
    'VL_VISIT': 'Followup 2 Viral Load',
    'VDATE': 'Followup 2 Viral Load Date',
})


print("Final merged with v12followup (first 5 rows):")
print(final_merged_with_v12.head())

# Optionally save the merged result
final_merged_with_v12.to_excel('~/Documents/KEMR/REPORTS/WP1/_2025_06_19_WP1_VL_DATA/WP1_VL_NIMR_KEMRI_DATA_FINAL_WITH_V12_2025_06_19.xlsx', index=False)
