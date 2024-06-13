import pandas as pd
from datetime import datetime
from category_encoders import MEstimateEncoder, OrdinalEncoder, TargetEncoder

# CSV 파일에서 데이터프레임 로드
file_path = 'DATA/org_crawling_data/total_apt_trade_data.csv'
df = pd.read_csv(file_path)

# 필요한 열만 선택하여 복사
selected_columns = ['아파트', '법정동', '도로명', '지역', '거래금액', '전용면적', '건축년도', '층']
df_selected = df[selected_columns].copy()

# 거래금액 열에서 쉼표 제거하고 숫자형으로 변환한 후 4개의 0 추가(만원 단위)
df_selected['거래금액'] = (df_selected['거래금액'].str.replace(',', '').astype(float) * 10000)

# 현재 연도 가져오기
current_year = datetime.now().year

# 년식 열 추가 및 Null 값 삭제, '건축년도' 열 삭제
df_selected['년식'] = current_year - df_selected['건축년도']
df_selected.dropna(inplace=True)
df_selected.drop(columns=['건축년도'], inplace=True)

# 열 순서 변경
df_selected = df_selected[['거래금액', '전용면적', '년식', '층', '아파트', '도로명', '법정동', '지역']]

# MEstimateEncoder, OrdinalEncoder, TargetEncoder 적용
encoders = {
    "MEstimate": MEstimateEncoder(cols=['아파트', '도로명', '법정동', '지역'], m=0.5),
    "Ordinal": OrdinalEncoder(cols=['아파트', '도로명', '법정동', '지역']),
    "Target": TargetEncoder(cols=['아파트', '도로명', '법정동', '지역'])
}

for encoder_name, encoder in encoders.items():
    df_encoded = encoder.fit_transform(df_selected, df_selected['거래금액'])
    for column in ['아파트', '도로명', '법정동', '지역']:
        new_column_name = f"{column}_{encoder_name}"
        df_selected[new_column_name] = df_encoded[column]

# 전처리된 DataFrame을 CSV 파일로 저장
output_file_path = 'DATA/preprocessed_data/first_preprocessed_data_org.csv'
df_selected.to_csv(output_file_path, index=False)

print("전처리된 데이터를 저장했습니다:", output_file_path)
print(df_selected.info())


