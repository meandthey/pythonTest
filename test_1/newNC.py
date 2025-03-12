import xarray as xr
import numpy as np
import pandas as pd
import os


file_path = "C:/Users/DESKTOP/Desktop/allData/기상청/태양광기상자원지도(평균수평면일사량)_월별/KMAPP_solar_FWS_01M_mean.nc"  # 여기에 한글 경로 입력

import netCDF4

file_path = "C:/사용자/내문서/KMAPP_solar_FWS_total_mean.nc"

try:
    nc_data = netCDF4.Dataset(file_path)  # NetCDF4 라이브러리로 직접 열어보기
    print("파일을 성공적으로 열었습니다.")
    print(nc_data)
except Exception as e:
    print("⚠ 파일을 열 수 없습니다. 오류:", e)


from pathlib import Path
import netCDF4

file_path = Path("C:/Users/DESKTOP/Desktop/allData/기상청/태양광기상자원지도(평균수평면일사량)_월별/KMAPP_solar_FWS_01M_mean.nc").resolve()

try:
    nc_data = netCDF4.Dataset(str(file_path))  # 경로를 문자열로 변환하여 전달
    print("파일을 성공적으로 열었습니다!")
except Exception as e:
    print("⚠ 파일을 열 수 없습니다. 오류:", e)



#import h5py

file_path = r"C:\Users\DESKTOP\Desktop\allData\기상청\태양광기상자원지도(평균수평면일사량)_월별\KMAPP_solar_FWS_01M_mean.nc"


#try:
#    with h5py.File(file_path, 'r') as f:
#        print(" 파일은 HDF5 형식입니다!")
#except Exception as e:
#    print("⚠ 이 파일은 HDF5 형식이 아닙니다. 오류:", e)


import xarray as xr

file_path = r"C:\Users\DESKTOP\Desktop\allData\기상청\태양광기상자원지도(평균수평면일사량)_월별\KMAPP_solar_FWS_01M_mean.nc"

ds = xr.open_dataset(file_path, engine="h5netcdf")  # HDF5 엔진 사용
print(ds)
