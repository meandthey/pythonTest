import xarray as xr
import pandas as pd
import os
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point




# NetCDF 파일들이 저장된 폴더 경로
#folder_path = "C:/Users/DESKTOP/Desktop/allData/KMA/solarResource_GHI_byMonth"
folder_path = "C:/Users/sidus/Desktop/solarResource_GHI_byMonth"
# 1월~12월 NetCDF 파일 이름 리스트
file_names = [f"KMAPP_solar_FWS_{i:02d}M_mean.nc" for i in range(1, 13)]

# 최종 DataFrame 초기화
final_df = None

for month, file_name in enumerate(file_names, start=1):
    file_path = os.path.join(folder_path, file_name)

    rawData = xr.open_dataset(file_path, engine="netcdf4")

    irrData = rawData["SWDN_flat_with_shading"].to_dataframe().reset_index()

    irrData.rename(columns={"SWDN_flat_with_shading": f"value_{month}"}, inplace=True)

    if final_df is None:
        final_df = irrData
    else:
        final_df = final_df.merge(irrData, on=["Y", "X"], how="left")

# 최종 데이터 확인
print(final_df.head())

# CSV로 저장
#final_df.to_csv("final_data.csv", index=False)



# NetCDF 파일 열기
rawData_latlon_file_path = "C:/Users/sidus/Desktop/solarResource_GHI_byMonth/KMAP_latlon.nc"
rawData_latlon = xr.open_dataset(rawData_latlon_file_path)

# 데이터셋 구조 확인
print(rawData_latlon)

# 변수 목록 확인
print(rawData_latlon.variables)

# DataArray를 DataFrame으로 변환
latData = rawData_latlon['latitude'].values.flatten()
lonData = rawData_latlon['longitude'].values.flatten()

# DataFrame 생성
df_latlon = pd.DataFrame({"latitude": latData, "longitude": lonData})




########## Merge irrData and latlonData ##########
# 데이터프레임을 병합 (좌우 순서 유지)
merged_df = pd.concat([df_latlon, final_df], axis=1)

# 결측값(NaN) 제거
merged_df_clean = merged_df.dropna()

# value_1 ~ value_12의 합을 yearTotal 컬럼으로 추가
merged_df_clean['yearTotal'] = merged_df_clean.loc[:, 'value_1':'value_12'].sum(axis=1)


df_selected = merged_df_clean[['latitude', 'longitude', 'yearTotal']]



########## Shp file SGG  ##########
# SHP 파일 로드
shp_file = "C:/Users/sidus/Desktop/GRI Github/pythonTest/test_1/ctprvn_20230729/ctprvn.shp"  # 실제 파일 경로로 변경하세요
gdf_shp = gpd.read_file(shp_file)

# 좌표계를 EPSG:5179로 수동 설정
gdf_shp.set_crs("EPSG:5179", inplace=True)  # 또는 "EPSG:5181" 가능성 있음

# EPSG:4326 (WGS 84, 위경도 좌표계)로 변환
gdf_shp = gdf_shp.to_crs("EPSG:4326")


# 데이터 확인
print(gdf_shp.head())

# 지도 시각화
gdf_shp.plot(edgecolor="black", figsize=(8, 8))
plt.show()

df = df_selected

# GeoDataFrame 변환
geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
gdf_points = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")  # WGS84 좌표계 지정


# 3️⃣ 공간 조인: 시도 경계 안에 포함된 포인트만 추출
gdf_filtered = gpd.sjoin(gdf_points, gdf_shp, how="inner", predicate="within")

# 4️⃣ 결과 저장 & 출력
gdf_filtered.to_csv("filtered_data.csv", index=False)  # 파일로 저장
print(gdf_filtered.head())  # 데이터 일부 확인


print("시도 경계 좌표계:", gdf_shp.crs)
print("포인트 데이터 좌표계:", gdf_points.crs)
print(gdf_points[['latitude', 'longitude']].describe())


print(gdf_points.head())  # geometry 컬럼이 있는지 확인
print(gdf_points.geometry.head())  # Point 객체가 올바르게 생성되었는지 확인

import matplotlib.pyplot as plt

## 지도위에 점을 전부 뿌릴려면 너무 많다.
#fig, ax = plt.subplots(figsize=(8, 8))
#gdf_shp.plot(ax=ax, color="lightgrey", edgecolor="black")  # 시도 경계
#gdf_points.plot(ax=ax, color="red", markersize=1, alpha=0.5)  # 원본 포인트 데이터
#plt.show()




gdf_seoul = gdf_points[(gdf_points["longitude"] > 126) & (gdf_points["longitude"] < 127) &
                        (gdf_points["latitude"] > 37) & (gdf_points["latitude"] < 38)]

# 샘플링
gdf_sample_seoul = gdf_seoul.sample(n=3000, random_state=42)

# 지도 시각화
fig, ax = plt.subplots(figsize=(8, 8))
gdf_shp.plot(ax=ax, color="lightgrey", edgecolor="black")  # 시도 경계
gdf_sample_seoul.plot(ax=ax, color="blue", markersize=1, alpha=0.5)  # 서울 지역 포인트
plt.show()


### 잠재량 수치 확인

gdf_filtered['avgbyMonth'] = gdf_filtered['yearTotal'] / 12 * 8760

irr_total = gdf_filtered['avgbyMonth'].sum()

irr_total / 10**12 * 10**4