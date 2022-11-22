# import packages
import pandas as pd
import numpy as np

# dfY3_Q1_OD_GBV_CHALINZE = pd.read_excel('DATA_SORT/Year_Three/Quarter_One/Oct/Dar/GBV_ OCT 2021.xlsx', sheet_name='CHALINZE DC')
# dfY3_Q1_OD_GBV_ILALA = pd.read_excel('DATA_SORT/Year_Three/Quarter_One/Oct/Dar/GBV_ OCT 2021.xlsx', sheet_name='ILALA MC')
# dfY3_Q1_OD_GBV_LINDI = pd.read_excel('DATA_SORT/Year_Three/Quarter_One/Oct/Dar/GBV_ OCT 2021.xlsx', sheet_name='LINDI MC')
# dfY3_Q1_OD_GBV_MASASI = pd.read_excel('DATA_SORT/Year_Three/Quarter_One/Oct/Dar/GBV_ OCT 2021.xlsx', sheet_name='MASASI TC')
# dfY3_Q1_OD_GBV_MASASI2 = pd.read_excel('DATA_SORT/Year_Three/Quarter_One/Oct/Dar/GBV_ OCT 2021.xlsx', sheet_name='MASASI DC')
# dfY3_Q1_OD_GBV_MTAMA = pd.read_excel('DATA_SORT/Year_Three/Quarter_One/Oct/Dar/GBV_ OCT 2021.xlsx', sheet_name='MTAMA DC')
# dfY3_Q1_OD_GBV_NACHINGWEA = pd.read_excel('DATA_SORT/Year_Three/Quarter_One/Oct/Dar/GBV_ OCT 2021.xlsx', sheet_name='NACHINGWEA DC')
# dfY3_Q1_OD_GBV_MOSHI = pd.read_excel('DATA_SORT/Year_Three/Quarter_One/Oct/Dar/GBV_ OCT 2021.xlsx', sheet_name='MOSHI MC')
# dfY3_Q1_OD_GBV_RUANGWA = pd.read_excel('DATA_SORT/Year_Three/Quarter_One/Oct/Dar/GBV_ OCT 2021.xlsx', sheet_name='RUANGWA DC')
# dfY3_Q1_OD_GBV_TEMEKE = pd.read_excel('DATA_SORT/Year_Three/Quarter_One/Oct/Dar/GBV_ OCT 2021.xlsx', sheet_name='TEMEKE MC')


dfY3_Q1_OD_DAR_GBV_CHALINZE = pd.read_excel('DATA_SORT/Year_Three/Quarter_One/Oct/Dar/GBV_ OCT 2021.xlsx', sheet_name='CHALINZE DC')
dfY3_Q1_OD_DAR_GBV_CHALINZE = dfY3_Q1_OD_DAR_GBV_CHALINZE.iloc[19:49, :31]
dfY3_Q1_OD_DAR_GBV_CHALINZE['Region'] = 'Dar'

dfY3_Q1_OD_DOM_GBV_CHALINZE = pd.read_excel('DATA_SORT/Year_Three/Quarter_One/Oct/Dom/GBV_ OCT 2021.xlsx', sheet_name='CHALINZE DC')
dfY3_Q1_OD_DOM_GBV_CHALINZE = dfY3_Q1_OD_DOM_GBV_CHALINZE.iloc[19:49, :31]
dfY3_Q1_OD_DOM_GBV_CHALINZE['Region'] = 'Dom'
df = pd.concat([dfY3_Q1_OD_DAR_GBV_CHALINZE, dfY3_Q1_OD_DOM_GBV_CHALINZE], axis=0)

dfY3_Q1_OD_MBY_GBV_CHALINZE = pd.read_excel('DATA_SORT/Year_Three/Quarter_One/Oct/Mby/GBV_ OCT 2021.xlsx', sheet_name='CHALINZE DC')
dfY3_Q1_OD_MBY_GBV_CHALINZE = dfY3_Q1_OD_MBY_GBV_CHALINZE.iloc[19:49, :31]
dfY3_Q1_OD_MBY_GBV_CHALINZE['Region'] = 'MBY'
df = pd.concat([df, dfY3_Q1_OD_MBY_GBV_CHALINZE], axis=0)

dfY3_Q1_OD_MWZ_GBV_CHALINZE = pd.read_excel('DATA_SORT/Year_Three/Quarter_One/Oct/Mwz/GBV_ OCT 2021.xlsx', sheet_name='CHALINZE DC')
dfY3_Q1_OD_MWZ_GBV_CHALINZE = dfY3_Q1_OD_MWZ_GBV_CHALINZE.iloc[19:49, :31]
dfY3_Q1_OD_MWZ_GBV_CHALINZE['Region'] = 'MWZ'
df = pd.concat([df, dfY3_Q1_OD_MWZ_GBV_CHALINZE], axis=0)

df['Month'] = 'Oct'
df['Year'] = 'Year Three'
df['Quarter'] = 'Quarter One'


# tables = pd.pivot_table(df, values=None, index=['ZONE','MKOA','WILAYA','KATA'], columns=None, aggfunc='mean', fill_value=None, margins=False,
#                dropna=True, margins_name='All', observed=False, sort=True)[source]
# tables = pd.pivot_table(df, values=['ENEO'], index=['ZONE', 'MKOA','ENEO2', 'WILAYA', 'KATA', 'KIJIJI_MTAA'], fill_value=None,
#                         aggfunc='count', dropna=True)

print(df)
# writer = pd.ExcelWriter('BBC_REPORT.xlsx', engine='xlsxwriter')
# tables.to_excel(writer, sheet_name='BBC NIAMBIE TOOL  v.3.6')
# writer.save()
df.to_excel('DATA_SORT/GBV DATA.xlsx', index=False)







