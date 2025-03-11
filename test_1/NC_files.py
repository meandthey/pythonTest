import xarray as xr
import numpy as np
import pandas as pd


# NetCDF 파일 열기
file_path = "C:/Users/DESKTOP/Desktop/KMAPP_solar_FWS_total_mean.nc" # 여기에 .nc 파일 경로 입력
ds = xr.open_dataset(file_path)

# 데이터셋 구조 확인
print(ds)

# 변수 목록 확인
print(ds.variables)

# 특정 변수 데이터 확인

print(ds["SWDN_flat_with_shading"].shape)
print(ds["SWDN_flat_with_shading"].values)




# X (경도 격자) 및 Y (위도 격자) 값 가져오기
lon_values = ds["X"].values  # X (경도)
lat_values = ds["Y"].values  # Y (위도)
data_values = ds["SWDN_flat_with_shading"].values  # 태양 복사량 데이터

# 격자를 1D로 펼치기
lon_mesh, lat_mesh = np.meshgrid(lon_values, lat_values)
flat_lon = lon_mesh.ravel()
flat_lat = lat_mesh.ravel()
flat_data = data_values.ravel()

# DataFrame 생성 (경도, 위도, 값)```````````````
df = pd.DataFrame({"Longitude": flat_lon, "Latitude": flat_lat, "Value": flat_data})

# 결측값(NaN) 제거
df_cleaned = df.dropna()

# CSV 파일로 저장
csv_filename = "solar_radiation_data_cleaned.csv"
df_cleaned.to_csv(csv_filename, index=False, encoding="utf-8")

# 데이터 확인을 위해 표시
import ace_tools as tools
tools.display_dataframe_to_user(name="Cleaned Solar Radiation Data", dataframe=df_cleaned)

