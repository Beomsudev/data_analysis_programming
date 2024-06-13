import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 데이터 불러오기
file_path = 'DATA/preprocessed_data/first_preprocessed_data_org.csv'
df = pd.read_csv(file_path)

# 숫자 데이터만 추출
numeric_df = df.select_dtypes(include='number')

# 상관 계수 계산
correlation_matrix = numeric_df.corr()

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 히트맵 그리기
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('상관 계수 히트맵')
plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.tight_layout()

# 이미지 저장
output_file_path = 'DATA/image/03_dataAnalysisFirst/상관_계수_히트맵.png'
plt.savefig(output_file_path)
print("상관 계수 히트맵 이미지를 저장했습니다:", output_file_path)
