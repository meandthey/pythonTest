# pip install pandas
# pip install pandas openpyxl
# pip install tabulate
import pandas as pd
import numpy as np
import openpyxl

df = pd.read_excel("C:/Users/DESKTOP/Desktop/Github/platForm/태양광/data/assumption.xlsx", engine = 'openpyxl')

#print(df.head())


# Constants
km2_to_m2 = 10**6
TWh_to_kWh = 10**9
kor_area = 100210  # km2

print(km2_to_m2)



# File paths
rawData_irr_filePath = "C:/Users/DESKTOP/Desktop/allData/공공데이터포털"
excel_file = rawData_irr_filePath + "/한국에너지기술연구원_신재생자원지도데이터_태양자원_천리안1호_수평면전일사량_20191231_edit_bySGG.xlsx"
csv_file = rawData_irr_filePath + "/한국에너지기술연구원_신재생자원지도데이터_태양자원_천리안1호_수평면전일사량_20191231.csv"




# Reading data
rawData_mapping_latlong_to_SGG = pd.read_excel(excel_file, sheet_name="데이터")
rawData_irr_2012_to_2019 = pd.read_csv(csv_file, encoding='EUC-KR')

# Processing data
rawData_irr_2012_to_2019 = rawData_irr_2012_to_2019.melt(id_vars=['위도', '경도'], var_name='YYYYMM', value_name='value')

# Extract year from YYYYMM
rawData_irr_2012_to_2019['YYYY'] = rawData_irr_2012_to_2019['YYYYMM'].str.extract('(20\d{2})')

# Adjust values for each month
month_days = {'-01': 31, '-02': 28, '-03': 31, '-04': 30, '-05': 31, '-06': 30, '-07': 31, '-08': 31, '-09': 30, '-10': 31, '-11': 30, '-12': 31}
for month, days in month_days.items():
    rawData_irr_2012_to_2019.loc[rawData_irr_2012_to_2019['YYYYMM'].str.contains(month), 'value_per_month'] = rawData_irr_2012_to_2019['value'] * days

# Join with geographic data
full_data = pd.merge(rawData_irr_2012_to_2019, rawData_mapping_latlong_to_SGG, on=['위도', '경도'], how='left').dropna()

# Calculate area covered by each dot
unique_dots = full_data[['위도', '경도']].drop_duplicates()
area_per_dot = kor_area / len(unique_dots)  # km2

# Calculate value per month per km2
full_data['value_per_month_per_km2'] = full_data['value_per_month'] * area_per_dot * km2_to_m2

# Clean up YYYYMM column
full_data['YYYYMM'] = full_data['YYYYMM'].str.replace('[()]', '', regex=True).str.replace(' kWh per m2 per day', '')

# Select and rename columns
full_data = full_data[['위도', '경도', 'YYYYMM', 'YYYY', 'value_per_month_per_km2', 'CTP_KOR_NM', 'SIG_KOR_NM']]
full_data.rename(columns={'value_per_month_per_km2': 'value'}, inplace=True)

# Result
full_data.to_csv('example.csv', index=False, encoding = 'cp949')
