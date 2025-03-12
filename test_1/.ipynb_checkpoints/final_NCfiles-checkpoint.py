import xarray as xr
import pandas as pd
import os

# NetCDF 파일들이 저장된 폴더 경로
folder_path = "C:/Users/DESKTOP/Desktop/allData/KMA/solarResource_GHI_byMonth"

# 1월~12월 NetCDF 파일 이름 리스트
file_names = [f"KMAPP_solar_FWS_{i:02d}M_mean.nc" for i in range(1, 13)]

# 최종 DataFrame 초기화
final_df = None

for month, file_name in enumerate(file_names, start=1):
    file_path = os.path.join(folder_path, file_name)

    rawData = xr.open_dataset(file_path)

    irrData = rawData["SWDN_flat_with_shading"].to_dataframe().reset_index()

    irrData.rename(columns={"SWDN_flat_with_shading": f"value_{month}"}, inplace=True)

    if final_df is None:
        final_df = irrData
    else:
        final_df = final_df.merge(irrData, on=["Y", "X"], how="left")

# 최종 데이터 확인
print(final_df.head())

# CSV로 저장
final_df.to_csv("final_data.csv", index=False)

