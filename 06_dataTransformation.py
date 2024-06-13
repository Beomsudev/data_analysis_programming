import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# CSV 파일에서 데이터프레임 로드
file_path = 'DATA/preprocessed_data/first_preprocessed_data_org.csv'
df = pd.read_csv(file_path)

# 로그 변환 이전의 '거래금액'과 '전용면적'으로부터 상관 계수 계산
correlation_original = df['거래금액'].corr(df['전용면적'])
print(f"로그 변환 전 거래금액-전용면적 상관 계수: {correlation_original:.4f}")

# '거래금액' 열을 로그 변환
log_price = np.log1p(df['거래금액'])

# '전용면적' 열을 로그 변환
log_area = np.log1p(df['전용면적'])

# 로그 거래금액과 거래금액의 분포 비교
plt.figure(figsize=(20, 15))

# 거래금액 분포
plt.subplot(2, 2, 1)
sns.histplot(df['거래금액'], kde=True, color='purple')
plt.title('거래금액 분포')
plt.xlabel('거래금액')
plt.ylabel('빈도')

# 로그 거래금액 분포
plt.subplot(2, 2, 2)
sns.histplot(log_price, kde=True, color='green')
plt.title('로그 거래금액 분포')
plt.xlabel('로그 변환된 거래금액')
plt.ylabel('빈도')

# 전용면적 분포
plt.subplot(2, 2, 3)
sns.histplot(df['전용면적'], kde=True, color='blue')
plt.title('전용면적 분포')
plt.xlabel('전용면적')
plt.ylabel('빈도')

# 로그 전용면적 분포
plt.subplot(2, 2, 4)
sns.histplot(log_area, kde=True, color='orange')
plt.title('로그 전용면적 분포')
plt.xlabel('로그 변환된 전용면적')
plt.ylabel('빈도')

plt.tight_layout()
plt.savefig('DATA/image/06_dataTransformation/로그전후_분포.png')

# 로그 변환된 '거래금액'과 '전용면적'으로부터 상관 계수 계산
correlation_log = np.corrcoef(log_price, log_area)[0, 1]
print(f"로그 변환된 거래금액-전용면적 상관 계수: {correlation_log:.4f}")

# '거래금액'과 '전용면적'의 Z-Score 변환
zscore_price = stats.zscore(df['거래금액'])
zscore_area = stats.zscore(df['전용면적'])

# Z-Score 변환된 '거래금액'과 '전용면적'으로부터 상관 계수 계산
correlation_zscore = np.corrcoef(zscore_price, zscore_area)[0, 1]
print(f"Z-Score 변환된 거래금액-전용면적 상관 계수: {correlation_zscore:.4f}")

# 사분위법(IQR)을 사용하여 이상치 제거
Q1 = df[['거래금액', '전용면적']].quantile(0.25)
Q3 = df[['거래금액', '전용면적']].quantile(0.75)
IQR = Q3 - Q1

# IQR 범위 내의 데이터만 선택
df_no_outliers = df[~((df[['거래금액', '전용면적']] < (Q1 - 1.5 * IQR)) | (df[['거래금액', '전용면적']] > (Q3 + 1.5 * IQR))).any(axis=1)]

# 이상치 제거 후 상관 계수 계산
correlation_no_outliers = df_no_outliers['거래금액'].corr(df_no_outliers['전용면적'])
print(f"이상치 제거 후 거래금액-전용면적 상관 계수: {correlation_no_outliers:.4f}")

# 상관 계수 시각화
correlation_values = [correlation_original, correlation_log, correlation_zscore, correlation_no_outliers]
labels = ['원본', '로그 변환', 'Z-Score 변환', '사분위법(IQR)']

plt.figure(figsize=(10, 6))
bars = plt.bar(labels, correlation_values, color='skyblue')
plt.title('상관 계수')
plt.xlabel('변환 방법')
plt.ylabel('상관 계수 값')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()

# 각 막대 위에 상관 계수 값 표시
for bar, value in zip(bars, correlation_values):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f'{value:.4f}', ha='center', va='bottom')

# 그래프를 이미지 파일로 저장 (한글 파일명)
plt.savefig('DATA/image/06_dataTransformation/상관_계수_값.png')
