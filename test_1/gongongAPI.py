import requests
import math
import requests
import json

def lat_lon_to_grid(lat, lon):
    RE = 6371.00877  # 지구 반경(km)
    GRID = 5.0       # 격자 간격(km)
    SLAT1 = 30.0     # 투영 위도1(degree)
    SLAT2 = 60.0     # 투영 위도2(degree)
    OLON = 126.0     # 기준점 경도(degree)
    OLAT = 38.0      # 기준점 위도(degree)
    XO = 43          # 기준점 X좌표(GRID)
    YO = 136         # 기준점 Y좌표(GRID)

    DEGRAD = math.pi / 180.0

    re = RE / GRID
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = (sf ** sn * math.cos(slat1)) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / (ro ** sn)

    ra = math.tan(math.pi * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / (ra ** sn)
    theta = lon * DEGRAD - olon
    if theta > math.pi:
        theta -= 2.0 * math.pi
    if theta < -math.pi:
        theta += 2.0 * math.pi
    theta *= sn

    nx = math.floor(ra * math.sin(theta) + XO + 0.5)
    ny = math.floor(ro - ra * math.cos(theta) + YO + 0.5)
    return {'nx': nx, 'ny': ny}




# 발급받은 API 키
api_key = 'h57axkwWxz4B%2FtE0mRj0XQCVcxS15zrprY%2B915yjnWI255e19%2BYv1ypLnuLvhz5Xgq1LSafgPzJKQhagBFNNMQ%3D%3D'

# 조회할 날짜와 시간
base_date = '20200101'  # YYYYMMDD 형식
base_time = '1300'      # HHmm 형식

# 격자 좌표 (예: 서울)
coords = lat_lon_to_grid(37.5665, 126.9780)
nx = coords['nx']
ny = coords['ny']

# API 요청 URL
url = 'http://apis.data.go.kr/B551184/openapi/service/SolarGhiService/getSolarGhiHrInfo'
params = {
    'serviceKey': api_key,
    'numOfRows': 10,
    'pageNo': 1,
    'dataType': 'JSON',
    'base_date': base_date,
    'base_time': base_time,
    'nx': nx,
    'ny': ny
}

# API 요청
response = requests.get(url, params=params)
data = response.json()

# 결과 출력
print(data)
