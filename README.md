### 프로젝트 : 아파트 거래금액 상관 요소 분석
    목표 : 아파트 거래금액 데이터 분석을 통해 거래금액에 영향을 미치는 요소들 찾아보기
    
    사용 데이터
    1. 국토교통부_아파트매매 실거래 상세 자료 : https://www.data.go.kr/data/15057511/openapi.do
    2. Geocoder API 2.0 레퍼런스 : https://www.vworld.kr/dev/v4dv_geocoderguide2_s001.do

    
### 요구사항 및 라이브러리
    Python version : 3.11.7

    데이터 처리 및 분석
    numpy==1.26.4 # 다차원 배열 객체 및 수치 계산
    pandas==2.1.4 # 데이터 구조 및 데이터 분석 도구
    category_encoders==2.6.3 # 범주형 변수 인코딩 도구

    선형회귀 분석
    scikit-learn==1.2.2 # 선형 회귀 모델 및 데이터셋 분할 도구
    
    시각화
    matplotlib==3.8.0 # 데이터 시각화 도구
    seaborn==0.13.2 # 통계적 데이터 시각화 도구
    
    지도 시각화
    folium==0.16.0 # 대화형 지도를 만드는 도구
    
    웹 요청 및 XML 처리
    requests==2.31.0 # HTTP 요청을 보내고 응답을 받는 도구

### 코드 목차
    01_dataCrawling.py
    02_dataPreprocessing.py
    03_dataAnalysisFirst.py
    04_price_top_bot_check.py
    05_area_check.py
    06_dataTransformation.py
    07_dataResult_.py
    08_linearRegression.py
    09_getLatLon.py
    10_folium.py

### 동작 설명
    코드는 1~10을 순서대로 동작하여야 올바른 출력 결과값을 얻을 수 있습니다.
    용량이 큰 일부 csv 파일은 github 상에 올라가 있지 않습니다.

    01_dataCrawling.py
    동작 설명 :  
    입력 파일 : X
    출력 파일 : DATA/org_crawling_data/total_apt_trade_data.csv
    * API key 발급 필요
    
    02_dataPreprocessing.py
    동작 설명 : 각종 전처리 시행 후 csv 저장
    입력 파일 : DATA/org_crawling_data/total_apt_trade_data.csv
    출력 파일 : DATA/preprocessed_data/first_preprocessed_data_org.csv
    
    03_dataAnalysisFirst.py
    동작 설명 : 거래금액 상관계수 히트맵 저장
    입력 파일 : DATA/preprocessed_data/first_preprocessed_data_org.csv
    출력 파일 : DATA/image/03_dataAnalysisFirst/상관_계수_히트맵.png
    
    04_price_top_bot_check.py
    동작 설명 : 거래금액 상하위 1000개의 분포 막대 그래프 저장 / 거래금액 상하위 1000개의 분포 누적 막대 그래프 저장
    입력 파일 : DATA/preprocessed_data/first_preprocessed_data_org.csv
    출력 파일 : DATA/image/04_price_top_bot_check/상하위1000개_누적.png
                DATA/image/04_price_top_bot_check/상하위1000개_막대.png
                
    05_area_check.py
    동작 설명 : '전용면적' 20개 구간 분포 막대 그래프 저장
    입력 파일 : DATA/preprocessed_data/first_preprocessed_data_org.csv
    출력 파일 : DATA/image/05_area_check/전용면적_구간별_데이터개수.png
    
    06_dataTransformation.py
    동작 설명 : 로그 전후 분포 그래프 저장 / 각 이상치 제거 방법에 따른 상관계수치 막대 그래프 생성
    입력 파일 : DATA/preprocessed_data/first_preprocessed_data_org.csv
    출력 파일 : DATA/image/06_dataTransformation/로그전후_분포.png
                DATA/image/06_dataTransformation/상관_계수_값.png
    
    07_dataResult_.py
    동작 설명 : 4~6번 코드의 전처리 항목 적용한 csv 저장 / 전처리 전후 비교 히트맵 저장
    입력 파일 : DATA/preprocessed_data/first_preprocessed_data_org.csv
    출력 파일 : DATA/preprocessed_data/final_preprocessed_data.csv
                DATA/image/07_dataResult/최종히트맵.png
    
    08_linearRegression.py
    동작 설명 : 실행시 선형회귀분석 성능 모델 출력 / 각 요소별 가격 선형 상관 그래프 저장
    입력 파일 : DATA/preprocessed_data/final_preprocessed_data.csv
    출력 파일 : DATA/image/08_linearRegression/가격상관_그래프.png
    
    09_getLatLon.py
    동작 설명 : 실행시 수집한 아파트의 위도 경도 데이터 수집
    입력 파일 : DATA/org_crawling_data/total_apt_trade_data.csv
    출력 파일 : DATA/lat_lon_data/folium_data.csv
    * API key 발급 필요
    
    10_folium.py
    동작 설명 : 실행시 거래금액 high/low에 따라 히트맵 지도 생성
    입력 파일 : DATA/lat_lon_data/folium_data.csv
    출력 파일 : DATA/folium/heatmap.html

    
