import xarray as xr
import numpy as np
import pandas as pd
import os
import geopandas as gpd
import matplotlib.pyplot as plt

# NetCDF 파일 열기
rawData_file_path = "C:/Users/DESKTOP/Desktop/allData/KMA/solarResource_GHI_byMonth/KMAPP_solar_FWS_01M_mean.nc"
rawData = xr.open_dataset(rawData_file_path)

# 데이터셋 구조 확인
print(rawData)

# 변수 목록 확인
print(rawData.variables)

# 특정 변수 데이터 확인

print(rawData["SWDN_flat_with_shading"].shape)
print(rawData["SWDN_flat_with_shading"].values)


# DataArray를 DataFrame으로 변환
irrData = rawData["SWDN_flat_with_shading"].to_dataframe().reset_index()

irrData.to_csv("output_table.csv", index=False)



# NetCDF 파일 열기
rawData_latlon_file_path = "C:/Users/DESKTOP/Desktop/allData/KMA/solarResource_GHI_byMonth/appendix/KMAP_latlon.nc"
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

# 데이터 미리보기
print(df_latlon.head())


########## Merge irrData and latlonData ##########
# 데이터프레임을 병합 (좌우 순서 유지)
merged_df = pd.concat([df_latlon, irrData["SWDN_flat_with_shading"]], axis=1)

# 결측값(NaN) 제거
merged_df_clean = merged_df.dropna()

# 결과 확인
print(merged_df_clean.head())
print(merged_df_clean.tail())




########  행정구역 shp 파일
# 대한민국 행정구역 지도 데이터 (다운로드한 .shp 파일 경로 지정)
korea_map = gpd.read_file("./ctprvn_20230729/ctprvn.shp")

# 데이터 확인
print(korea_map.head())

# Shapefile 불러오기
# 현재 좌표계 확인
print(korea_map.crs)

# 원래 좌표계를 EPSG:5179로 설정
korea_map = korea_map.set_crs(epsg=5179)

# EPSG:4326 (WGS84)로 변환
korea_map = korea_map.to_crs(epsg=4326)

# 변환된 데이터 확인
print(korea_map.crs)

# 지도 플롯
fig, ax = plt.subplots(figsize=(10, 10))
korea_map.plot(ax=ax, color="lightgray", edgecolor="black")  # 지도 색상 설정

# 각 지역(도시) 이름 추가
for idx, row in korea_map.iterrows():
    ax.annotate(row["CTP_ENG_NM"], xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                ha="center", fontsize=8, color="red")

plt.title("대한민국 행정구역 지도", fontsize=15)
plt.show()


### 행정구역 경계 위에 포인트 찍기
sample_mergedf_clean_sample = merged_df_clean.sample(n=5000, random_state=42)

# 3️⃣ 지도 생성
fig, ax = plt.subplots(figsize=(10, 10))

# 대한민국 행정구역 지도 그리기
korea_map.plot(ax=ax, color="lightgray", edgecolor="black")

# 4️⃣ 위경도 데이터 점 찍기 (색상: 값(SWDN_flat_with_shading) 기준)
sc = ax.scatter(sample_mergedf_clean_sample["longitude"], sample_mergedf_clean_sample["latitude"], 
                c=sample_mergedf_clean_sample["SWDN_flat_with_shading"], cmap="jet", s=50, edgecolors="black", alpha=0.7)

# 5️⃣ 컬러바 추가
plt.colorbar(sc, label="SWDN_flat_with_shading (W/m²)")

# 6️⃣ 그래프 설정
plt.title("대한민국 지도 + 위경도 데이터", fontsize=15)
plt.xlabel("경도 (Longitude)")
plt.ylabel("위도 (Latitude)")
plt.show()
################################################################################################################################################
########## Visualize 1 ##########
import folium

# 중심 좌표 (데이터의 평균값 사용)
map_center = [merged_df_clean["latitude"].mean(), merged_df_clean["longitude"].mean()]

# 지도 생성
m = folium.Map(location=map_center, zoom_start=10)

# 데이터 점 찍기
for idx, row in merged_df_clean.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=3,  # 원 크기
        color="blue",  # 점 색깔
        fill=True,
        fill_color="blue",
        fill_opacity=0.5,
        popup=f"일사량: {row['SWDN_flat_with_shading']:.2f} W/m²"
    ).add_to(m)




    # 데이터 샘플링 (5000개만 선택)
sample_df = merged_df_clean.sample(n=5000, random_state=42)

print(f"샘플링 후 반복 횟수: {sample_df.shape[0]}")

# 샘플링된 데이터만 지도에 표시
for idx, row in sample_df.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=2,  # 원 크기
        color="blue",  # 점 색깔
        fill=True,
        fill_color="blue",
        fill_opacity=0.5,
        popup=f"일사량: {row['SWDN_flat_with_shading']:.2f} W/m²"
    ).add_to(m)

# 지도 저장 및 출력
m.save("irradiance_map_sampled.html")
    


########## Visualize 2 ##########
import matplotlib.pyplot as plt

# 산점도 플롯 (일사량에 따라 색상 변경)
plt.figure(figsize=(10, 8))
plt.scatter(
    sample_df["longitude"], sample_df["latitude"], 
    c=sample_df["SWDN_flat_with_shading"], cmap="jet", alpha=0.7, s=5
)

plt.colorbar(label="일사량 (W/m²)")
plt.xlabel("경도 (Longitude)")
plt.ylabel("위도 (Latitude)")
plt.title("태양 복사 일사량 지도")

plt.show()



########## Visualize 3 ##########
import geopandas as gpd

# 지도 데이터 불러오기 (대한민국 지도)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# 데이터 확인
print(world.head())


# DataFrame을 GeoDataFrame으로 변환
gdf = gpd.GeoDataFrame(
    merged_df_clean, geometry=gpd.points_from_xy(merged_df_clean.longitude, merged_df_clean.latitude)
)

# 지도 그리기
fig, ax = plt.subplots(figsize=(10, 8))
world.plot(ax=ax, color="lightgray")  # 배경 지도
gdf.plot(ax=ax, column="SWDN_flat_with_shading", cmap="jet", markersize=5, alpha=0.7, legend=True)

plt.title("태양 복사 일사량 지도")
plt.show()




########## Visualize 4 ##########
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
import ssl
import requests
import certifi
import os

# 🔹 SSL 인증서 문제 해결
ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()
os.environ["SSL_CERT_FILE"] = certifi.where()

# 🔹 세계 지도 데이터 로드 (GeoPandas)
world = gpd.read_file("https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip")

# 🔹 지도 플롯
fig, ax = plt.subplots(figsize=(10, 6))
world.plot(ax=ax, color="lightgray", edgecolor="black")

# 🔹 Contextily 지도 추가 (줌 레벨 제한)
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=10)

plt.show()









# 1️⃣ 대한민국 행정구역 지도 불러오기
korea_map = gpd.read_file("./ctprvn_20230729/ctprvn.shp").to_crs(epsg=4326)

# 2️⃣ 위경도 + 값이 포함된 데이터 예제 (위치 데이터)
data = pd.DataFrame({
    "latitude": [37.5665, 35.1796, 36.3504, 35.8714, 37.4563],  # 서울, 부산, 대전, 대구, 인천
    "longitude": [126.9780, 129.0756, 127.3845, 128.6014, 126.7052],
    "value": [100, 200, 150, 180, 90]  # 예제 값 (예: 일사량, 온도 등)
})

# 3️⃣ 지도 그리기
fig, ax = plt.subplots(figsize=(10, 10))
korea_map.plot(ax=ax, color="lightgray", edgecolor="black")  # 대한민국 지도

# 4️⃣ 위경도 데이터 점 찍기 (색상 크기 조절 가능)
sc = ax.scatter(data["longitude"], data["latitude"], 
                c=data["value"], cmap="coolwarm", s=100, edgecolors="black", alpha=0.7)

# 5️⃣ 값 표시 (점 위에 숫자 추가)
for i, row in data.iterrows():
    ax.text(row["longitude"], row["latitude"], f"{row['value']}", fontsize=10, ha='center', color="black")

# 6️⃣ 컬러바 추가 (값에 따른 색 변화)
plt.colorbar(sc, label="값 (예: 일사량, 온도 등)")
plt.title("대한민국 지도 + 위경도 데이터", fontsize=15)
plt.xlabel("경도 (Longitude)")
plt.ylabel("위도 (Latitude)")
plt.show()