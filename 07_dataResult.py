import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# CSV 파일에서 데이터프레임 로드
file_path = 'DATA/preprocessed_data/first_preprocessed_data_org.csv'
df = pd.read_csv(file_path)

# 음수 값을 가진 행 제거
df = df[df['층'] >= 0]

# 선택된 열만으로 새로운 데이터프레임 생성
selected_columns = ['거래금액', '전용면적', '년식', '층', '아파트_Target', '도로명_Target', '법정동_Target', '지역_Target']
df_selected = df[selected_columns]

# 데이터프레임의 첫 몇 행 확인
print(df_selected.head())

# 히트맵을 위한 상관관계 행렬 계산
corr_original = df_selected.corr()

# 거래금액을 기준으로 데이터프레임을 오름차순으로 정렬
df_selected_sorted = df_selected.sort_values(by='거래금액')

# 상위 50개와 하위 100개를 삭제
df_selected_trimmed = df_selected_sorted.iloc[50:-100].copy()

# 거래금액을 로그화
df_selected_trimmed['로그_거래금액'] = np.log(df_selected_trimmed['거래금액'])
df_selected_trimmed['로그_전용면적'] = np.log(df_selected_trimmed['전용면적'])
df_selected_trimmed['로그_년식'] = np.log(df_selected_trimmed['년식'])
df_selected_trimmed['로그_층'] = np.log(df_selected_trimmed['층'])
df_selected_trimmed['로그_아파트'] = np.log(df_selected_trimmed['아파트_Target'])
df_selected_trimmed['로그_도로명'] = np.log(df_selected_trimmed['도로명_Target'])
df_selected_trimmed['로그_법정동'] = np.log(df_selected_trimmed['법정동_Target'])
df_selected_trimmed['로그_지역'] = np.log(df_selected_trimmed['지역_Target'])

# 기존 열 드랍
df_selected_trimmed = df_selected_trimmed.drop(['거래금액', '전용면적', '년식', '층', '아파트_Target', '도로명_Target', '법정동_Target', '지역_Target'], axis=1)

# 히트맵을 위한 상관관계 행렬 계산 (로그화된 데이터)
corr_log = df_selected_trimmed.corr()

# 서브플롯 생성
fig, axes = plt.subplots(1, 2, figsize=(20, 8))

# 원본 데이터 히트맵
sns.heatmap(corr_original, annot=True, cmap='coolwarm', fmt=".2f", ax=axes[0])
axes[0].set_title('원본 데이터 Heatmap')

# 로그 데이터 히트맵
sns.heatmap(corr_log, annot=True, cmap='coolwarm', fmt=".2f", ax=axes[1])
axes[1].set_title('형태변화 데이터 Heatmap')
plt.xticks(rotation=45)
plt.show()

# 이미지 저장
plt.savefig('DATA/image/07_dataResult/최종히트맵.png')

# 최종 전처리된 데이터프레임을 CSV 파일로 저장
final_file_path = 'DATA/preprocessed_data/final_preprocessed_data.csv'
df_selected_trimmed.to_csv(final_file_path, index=False)

# 결과값 출력
print("최종 전처리된 데이터프레임:")
print(df_selected_trimmed.head())
print("\n최종 전처리된 데이터프레임의 상관관계 히트맵 이미지가 저장되었습니다.")
print("최종 전처리된 데이터프레임이 CSV 파일로 저장되었습니다.")
