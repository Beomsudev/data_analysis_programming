import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 함수: 거래금액을 원하는 형식으로 표기하는 함수
def format_price(price):
    if price < 1e4:
        return f"{price:.0f}원"
    elif price < 1e8:
        return f"{price/1e4:.0f}만원"
    elif price < 1e9:
        man = int(price // 1e4) % 10000
        return f"{int(price // 1e8)}억 {man}만원"
    elif price < 1e10:
        return f"{price/1e8:.0f}억원"
    else:
        return "Unknown"

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# Load the preprocessed data
preprocessed_file_path = 'DATA/preprocessed_data/first_preprocessed_data_org.csv'
df_preprocessed = pd.read_csv(preprocessed_file_path)

# Access the '거래금액' column
거래금액 = df_preprocessed['거래금액']

# 거래금액을 오름차순으로 정렬
거래금액_sorted = 거래금액.sort_values()

# 거래금액을 10개의 구간으로 나누기
bin_counts, bin_edges = np.histogram(거래금액_sorted, bins=10)

# 각 구간의 범위와 데이터 개수 출력
print("전체 데이터의 구간별 거래금액 분포")
for i in range(len(bin_counts)):
    start = format_price(bin_edges[i])
    end = format_price(bin_edges[i + 1])
    count = bin_counts[i]
    print(f"구간 {i + 1}: {start} ~ {end}, 데이터 개수: {count}")

# 상위 1000개 데이터 선택
상위1000데이터 = 거래금액_sorted[-1000:]

# 하위 1000개 데이터 선택
하위1000데이터 = 거래금액_sorted[:1000]

# 상위 1000개 데이터를 10개의 구간으로 나누기
bin_counts_top_1000, bin_edges_top_1000 = np.histogram(상위1000데이터, bins=10)

# 하위 1000개 데이터를 10개의 구간으로 나누기
bin_counts_bottom_1000, bin_edges_bottom_1000 = np.histogram(하위1000데이터, bins=10)

# 각 구간의 범위와 데이터 개수 출력
print("\n상위 1000개 데이터의 구간별 거래금액 분포")
for i in range(len(bin_counts_top_1000)):
    start = format_price(bin_edges_top_1000[i])
    end = format_price(bin_edges_top_1000[i + 1])
    count = bin_counts_top_1000[i]
    print(f"구간 {i + 1}: {start} ~ {end}, 데이터 개수: {count}")

print("\n하위 1000개 데이터의 구간별 거래금액 분포")
for i in range(len(bin_counts_bottom_1000)):
    start = format_price(bin_edges_bottom_1000[i])
    end = format_price(bin_edges_bottom_1000[i + 1])
    count = bin_counts_bottom_1000[i]
    print(f"구간 {i + 1}: {start} ~ {end}, 데이터 개수: {count}")

# 막대 그래프 그리기
plt.figure(figsize=(15, 6))

# 하위 1000개의 데이터 그래프
plt.subplot(1, 2, 1)
bars_bottom = plt.bar(range(len(bin_counts_bottom_1000)), bin_counts_bottom_1000, tick_label=[f'{format_price(bin_edges_bottom_1000[i])} ~ {format_price(bin_edges_bottom_1000[i+1])}' for i in range(len(bin_counts_bottom_1000))])
plt.title('하위 1000개의 데이터 분포')
plt.xlabel('거래금액')
plt.ylabel('데이터 개수')
plt.xticks(rotation=45, ha='right')  # x축 레이블 회전 및 정렬
plt.grid(True)

# 각 막대 위에 데이터 개수 표시
for bar, count in zip(bars_bottom, bin_counts_bottom_1000):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(count), ha='center', va='bottom')

# 상위 1000개의 데이터 그래프
plt.subplot(1, 2, 2)
bars_top = plt.bar(range(len(bin_counts_top_1000)), bin_counts_top_1000, tick_label=[f'{format_price(bin_edges_top_1000[i])} ~ {format_price(bin_edges_top_1000[i+1])}' for i in range(len(bin_counts_top_1000))])
plt.title('상위 1000개의 데이터 분포')
plt.xlabel('거래금액')
plt.ylabel('데이터 개수')
plt.xticks(rotation=45, ha='right')  # x축 레이블 회전 및 정렬
plt.grid(True)

# 각 막대 위에 데이터 개수 표시
for bar, count in zip(bars_top, bin_counts_top_1000):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(count), ha='center', va='bottom')

plt.tight_layout()
plt.savefig('DATA/image/04_price_top_bot_check/상하위1000개_막대.png')

# 누적 막대 그래프 그리기
plt.figure(figsize=(15, 6))

# 하위 1000개의 데이터 그래프
plt.subplot(1, 2, 1)
cumulative_bottom = np.cumsum(bin_counts_bottom_1000)
bars_bottom = plt.bar(range(len(bin_counts_bottom_1000)), cumulative_bottom, tick_label=[f'{format_price(bin_edges_bottom_1000[i])} ~ {format_price(bin_edges_bottom_1000[i+1])}' for i in range(len(bin_counts_bottom_1000))])
plt.title('하위 1000개의 데이터 분포 (누적)')
plt.xlabel('거래금액')
plt.ylabel('데이터 개수')
plt.xticks(rotation=45, ha='right')  # x축 레이블 회전 및 정렬
plt.grid(True)

# 각 막대 위에 누적된 데이터 개수 표시
for bar, count in zip(bars_bottom, cumulative_bottom):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(int(count)), ha='center', va='bottom')

# 상위 1000개의 데이터 그래프 (역순)
plt.subplot(1, 2, 2)
cumulative_top_reverse = np.cumsum(bin_counts_top_1000[::-1])[::-1]  # 상위 데이터의 누적값을 역순으로 계산
bars_top = plt.bar(range(len(bin_counts_top_1000)), cumulative_top_reverse, tick_label=[f'{format_price(bin_edges_top_1000[i])} ~ {format_price(bin_edges_top_1000[i+1])}' for i in range(len(bin_counts_top_1000))])
plt.title('상위 1000개의 데이터 분포 (누적, 역순)')
plt.xlabel('거래금액')
plt.ylabel('데이터 개수')
plt.xticks(rotation=45, ha='right')  # x축 레이블 회전 및 정렬
plt.grid(True)

# 각 막대 위에 누적된 데이터 개수 표시
for bar, count in zip(bars_top, cumulative_top_reverse):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(int(count)), ha='center', va='bottom')

plt.tight_layout()
plt.savefig('DATA/image/04_price_top_bot_check/상하위1000개_누적.png')