import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# CSV 파일에서 데이터프레임 로드
file_path = 'DATA/preprocessed_data/first_preprocessed_data_org.csv'
df = pd.read_csv(file_path)

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 전용면적을 20개의 구간으로 나누기
bin_counts, bin_edges = np.histogram(df['전용면적'], bins=20)

# 각 구간의 범위와 데이터 개수 출력
print("전체 데이터의 구간별 전용면적 분포")
for i in range(len(bin_counts)):
    start = bin_edges[i]
    end = bin_edges[i + 1]
    count = bin_counts[i]
    print(f"구간 {i + 1}: {start:.2f} ~ {end:.2f} (제곱미터), 데이터 개수: {count}")

# 막대 그래프 그리기
plt.figure(figsize=(10, 6))
bars = plt.bar(range(len(bin_counts)), bin_counts, tick_label=[f'{start:.2f} ~ {end:.2f}' for start, end in zip(bin_edges[:-1], bin_edges[1:])])
plt.title('전용면적 구간별 데이터 개수')
plt.xlabel('전용면적 (제곱미터)')
plt.ylabel('데이터 개수')
plt.xticks(rotation=45, ha='right')  # x축 레이블 회전 및 정렬

# 각 막대 위에 데이터 개수 표시
for bar, count in zip(bars, bin_counts):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(count), ha='center', va='bottom')

plt.tight_layout()

# 그래프를 이미지로 저장
output_file_path = 'DATA/image/05_area_check/전용면적_구간별_데이터개수.png'
plt.savefig(output_file_path)

# 결과 출력
print("전용면적 구간별 데이터 개수 그래프를 저장했습니다:", output_file_path)
