url <- 'https://apihub.kma.go.kr/api/file?authKey=JL2v5ZFTScK9r-WRU8nCNA'; # 다운로드할 파일의 URL 설정
file_path <- 'output_file.zip'; # 저장할 파일 경로 설정
download.file(url, file_path, mode = 'wb'); # URL에서 파일 다운로드
