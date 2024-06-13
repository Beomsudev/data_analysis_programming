import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns


# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

print("=====전처리전=====")
# CSV 파일에서 데이터프레임 로드
file_path = 'DATA/preprocessed_data/first_preprocessed_data_org.csv'
df = pd.read_csv(file_path)

# 음수 값을 가진 행 제거
df = df[df['층'] >= 0]

# 선택된 열만으로 새로운 데이터프레임 생성
selected_columns = ['거래금액', '전용면적', '년식', '층', '아파트_Target', '도로명_Target', '법정동_Target', '지역_Target']
df_selected = df[selected_columns]

# 독립변수와 종속변수 분리
X_selected = df_selected.drop(columns=['거래금액'])  # 독립변수
y_selected = df_selected['거래금액']  # 종속변수

# 훈련 세트와 테스트 세트로 데이터 분할
X_train_selected, X_test_selected, y_train_selected, y_test_selected = train_test_split(X_selected, y_selected, test_size=0.2, random_state=42)

# 선형 회귀 모델 생성
model_selected = LinearRegression()

# 모델 훈련
model_selected.fit(X_train_selected, y_train_selected)

# 테스트 세트를 사용하여 예측
y_pred_selected = model_selected.predict(X_test_selected)

# 모델 성능 평가
mse_selected = mean_squared_error(y_test_selected, y_pred_selected)
rmse_selected = np.sqrt(mse_selected)
r2_selected = r2_score(y_test_selected, y_pred_selected)
print("MSE (Selected):", mse_selected)
print("R^2 Score (Selected):", r2_selected)
print("RMSE (Selected):", rmse_selected)

print('Y 절편 값 (Selected):', np.round(model_selected.intercept_, 3))
print('회귀 계수 값 (Selected):', np.round(model_selected.coef_, 3))

y_train_pred_selected = model_selected.predict(X_train_selected)
y_test_pred_selected = model_selected.predict(X_test_selected)
print('R^2 score (학습데이터) (Selected):', r2_score(y_train_selected, y_train_pred_selected))
print('R^2 score (테스트데이터) (Selected):', r2_score(y_test_selected, y_test_pred_selected))

print("=====전처리후=====")
# CSV 파일 읽기
file_path = 'DATA/preprocessed_data/final_preprocessed_data.csv'
data = pd.read_csv(file_path)

# 독립변수와 종속변수 분리
X = data.drop(columns=['로그_거래금액'])  # 독립변수
y = data['로그_거래금액']  # 종속변수

# 훈련 세트와 테스트 세트로 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 선형 회귀 모델 생성
model = LinearRegression()

# 모델 훈련
model.fit(X_train, y_train)

# 테스트 세트를 사용하여 예측
y_pred = model.predict(X_test)

# 모델 성능 평가
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)
print("MSE:", mse)
print("R^2 Score:", r2)
print("RMSE:", rmse)

print('Y 절편 값:', np.round(model.intercept_, 3))
print('회귀 계수 값:', np.round(model.coef_, 3))

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)
print('R^2 score (학습데이터):', r2_score(y_train, y_train_pred))
print('R^2 score (테스트데이터):', r2_score(y_test, y_test_pred))

# 데이터 샘플링
sample_data = data.sample(frac=0.1, random_state=42)  # 10% 샘플링

# 그래프 플로팅 및 저장
fig, axs = plt.subplots(figsize=(18, 18), ncols=3, nrows=3)
features = ['로그_전용면적', '로그_년식', '로그_층', '로그_아파트', '로그_도로명', '로그_법정동', '로그_지역']
plot_color = ['r', 'g', 'b', 'y', 'c', 'm', 'k']

# 투명도를 조정한 그래프 플로팅 및 저장
fig, axs = plt.subplots(figsize=(18, 18), ncols=3, nrows=3)
for i, f in enumerate(features):
    row = int(i / 3)
    col = i % 3
    sns.regplot(x=f, y='로그_거래금액', data=data, ax=axs[row][col], color=plot_color[i], scatter_kws={'alpha':0.3})

# 빈 서브플롯 삭제
if len(features) < 9:
    for j in range(len(features), 9):
        fig.delaxes(axs.flat[j])

plt.tight_layout()
plt.savefig('DATA/image/08_linearRegression/가격상관_그래프.png')
plt.show()

plt.show()