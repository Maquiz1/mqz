import pandas as pd
import os

# Load client data
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

# Display selected columns from client data, with facility as the first column (drop site_id)
client_columns = ['facility', 'id', 'enrollment_id', 'vl', 'vl_date', 'recent_vl', 'recent_vl_date']
df_client_selected = df_client[client_columns]

# # Load visit data
# csv_visit_path = '~/Documents/KEMR/DATA_NIMR/visit_2025_0619.csv'
# visit_path = os.path.expanduser(csv_visit_path)
# df_visit = pd.read_csv(visit_path)

# # Display selected columns from visit data
# visit_columns = ['client_id', 'visit_name', 'visit_date', 'vl_results', 'sample_date', 'sample_date6', 'vl_results6']
# df_visit_selected = df_visit[visit_columns]

# # Merge client and visit data on id (client) and client_id (visit)
# df_client_selected['id'] = df_client_selected['id'].astype(str)
# df_visit_selected['client_id'] = df_visit_selected['client_id'].astype(str)
# merged = pd.merge(df_client_selected, df_visit_selected, left_on='id', right_on='client_id', how='inner')

# # Drop 'client_id' and 'id', and reorder columns: facility, visit_name, visit_date, ...
# final_columns = ['facility', 'visit_name', 'visit_date', 'enrollment_id', 'vl', 'vl_date', 'recent_vl', 'recent_vl_date', 'vl_results', 'sample_date', 'sample_date6', 'vl_results6']
# merged = merged[final_columns]

# Sort by enrollment_id
merged = df_client_selected.sort_values(by='enrollment_id')

print("\nMerged data (first 5 rows):")
print(merged.head())

# Optionally save the merged result
merged.to_excel('~/Documents/KEMR/REPORTS/WP1/_2025_06_20_WP1_VL_DATA/WP1_VL_CLIENTS_NIMR_DATA_2025_06_20.xlsx', index=False)
