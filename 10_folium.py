import folium
import pandas as pd
from folium.plugins import HeatMap

# CSV 파일 불러오기
df = pd.read_csv("DATA/lat_lon_data/folium_data.csv")

# 년, 월, 일 합친 날짜 컬럼 생성
df['년월일'] = df['년'] * 10000 + df['월'] * 100 + df['일']

# 2020년 이전 데이터 제거
df = df[df['년월일'] >= 20230101]

# 거래금액 열의 문자열 형식 수정 (쉼표 제거 및 숫자로 변환)
df['거래금액'] = df['거래금액'].str.replace(',', '').astype(int)

# Heatmap을 위한 데이터 포맷으로 변환
heat_data = [[row['위도'], row['경도'], row['거래금액']] for index, row in df.iterrows()]

# Folium 지도 객체 생성
m = folium.Map(location=[df['위도'].mean(), df['경도'].mean()], zoom_start=12)

# Heatmap 추가
HeatMap(heat_data,
        gradient={0.2: 'blue', 0.4: 'cyan', 0.6: 'lime', 0.8: 'yellow', 1: 'red'},
        radius=15, blur=10, max_zoom=15, min_opacity=0.5).add_to(m)

# 지도를 HTML 파일로 저장
m.save('DATA/folium/heatmap.html')
