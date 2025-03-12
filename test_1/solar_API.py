import pandas as pd
import requests

API_KEY = 'JL2v5ZFTScK9r-WRU8nCNA'

base_url = "https://apihub.kma.go.kr/api/typ01/cgi-bin/sat/nph-sat_ana_txt?"
params = {
    "tm": "202107101600",
    "obs": "si_ai",
    "help": "0",
    "authKey": API_KEY
}

outFile = "C:/Users/DESKTOP/Desktop/Github/python/test_1/OutputFile.zip"

response = requests.get(base_url, params=params, verify=False)
response.encoding = 'euc-kr'
# response.text는 네가 받은 데이터 텍스트
raw_text = response.text.replace('\n', '').strip()

# with open("outputFileEUCDataList1600.txt", "w", encoding = 'euc-kr') as f:
#     f.write(raw_text)

# print("처음 100자:", repr(raw_text[:100]))
# print("마지막 100자:", repr(raw_text[-100:]))

# 데이터에서 쉼표(,) 기준으로 숫자 추출
data_list = raw_text.split(',')

print("처음 100자:", repr(data_list[:100]))
print("마지막 100자:", repr(data_list[-100:]))

# 불필요한 공백 제거, 숫자형으로 변환 (첫번째 값은 보통 데이터 길이거나 인덱스일 수 있음)
data_list = [float(x.strip()) for x in data_list[1:] if x.strip() != '']


# with open("outputFileDataList.txt", "w", encoding = 'euc-kr') as f:
#     f.write(data_list)
with open("outputFileDataList.txt", "w", encoding='euc-kr') as f:
    f.write("\n".join(map(str, data_list)))  # 리스트를 문자열로 변환하여 저장



# 데이터프레임으로 변환 (예시: 열 개수 10개로 나누기)
df = pd.DataFrame([data_list[i:i+10] for i in range(0, len(data_list), 10)])

print(df.head())  # 처음 몇 줄 확인


if response.status_code == 200:
    with open(outFile, "wb") as f:
        f.write(response.content)
    print("정상 다운로드 완료!")
else:
    print(f"오류 발생! 상태코드: {response.status_code}")
    print(response.text)






import numpy as np
import pandas as pd

# 기준 경도/위도 (중앙 기준점)
base_lon, base_lat = 126.0, 38.0

# 격자 크기 (2km 간격)
grid_size_km = 2  # km
grid_size_m = grid_size_km * 1000  # meter

# 경도/위도 변환 기준 (1도 ≈ 111km)
km_per_degree = 111  # 1도의 길이 (약 111km)

# 900x900 격자 생성
grid_x = np.arange(-450, 450) * grid_size_km  # 동서 방향 이동 (km)
grid_y = np.arange(-450, 450) * grid_size_km  # 남북 방향 이동 (km)

# 위경도 변환
lon_grid = base_lon + (grid_x / km_per_degree)  # 경도 변화
lat_grid = base_lat + (grid_y / km_per_degree)  # 위도 변화

# 격자로 변환
lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)

# 데이터프레임 생성
df = pd.DataFrame({
    "Latitude": lat_mesh.ravel(),  # 위도 (북->남)
    "Longitude": lon_mesh.ravel(),  # 경도 (서->동)
    "Grid_X": np.tile(np.arange(900), 900),  # 격자 X 인덱스
    "Grid_Y": np.repeat(np.arange(900), 900)  # 격자 Y 인덱스
})

# 결과 출력
#import ace_tools as tools
#tools.display_dataframe_to_user(name="900x900 Grid Coordinates", dataframe=df)
