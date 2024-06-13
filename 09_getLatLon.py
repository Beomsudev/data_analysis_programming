import os
import datetime
import pandas as pd
import requests


class AddressGeocoder:
    def __init__(self, csv_file_path, api_key):
        self.csv_file_path = csv_file_path
        self.api_key = api_key
        self.address_csv_path = 'DATA/lat_lon_data/address_data.csv'
        self.log_dir = 'DATA/lat_lon_data'

    def create_address_csv(self):
        # CSV 파일을 pandas 데이터 프레임으로 불러오기
        data = pd.read_csv(self.csv_file_path)

        # 필요한 컬럼만 추출하여 새로운 데이터프레임 생성
        selected_columns = ['거래금액', '전용면적', '건축년도', '층', '아파트', '도로명', '도로명건물본번호코드', '도로명건물부번호코드', '년', '월', '일']
        new_data = data[selected_columns].copy()

        # NaN 값을 0으로 대체
        new_data.loc[:, '도로명건물본번호코드'] = new_data['도로명건물본번호코드'].fillna(0)
        new_data.loc[:, '도로명건물부번호코드'] = new_data['도로명건물부번호코드'].fillna(0)

        # 새로운 컬럼 '도로명주소' 생성
        def create_road_address(row):
            road_name = row['도로명']
            main_code = int(row['도로명건물본번호코드'])
            sub_code = int(row['도로명건물부번호코드'])
            if sub_code == 0:
                return f"{road_name} {main_code}"
            else:
                return f"{road_name} {main_code}-{sub_code}"

        new_data.loc[:, '도로명주소'] = new_data.apply(create_road_address, axis=1)

        # 불필요한 컬럼 드랍
        new_data.drop(columns=['도로명', '도로명건물본번호코드', '도로명건물부번호코드'], inplace=True)

        # 결과를 CSV 파일로 저장
        new_data.to_csv(self.address_csv_path, index=False)

    def remove_duplicate_addresses(self):
        # CSV 파일을 불러와서 도로명 주소를 기준으로 중복값 제거
        unique_address_data = pd.read_csv(self.address_csv_path)
        unique_address_data.drop_duplicates(subset=['도로명주소'], inplace=True)
        unique_address_data.reset_index(drop=True, inplace=True)  # 인덱스를 다시 설정하고 기존 인덱스를 버림
        print(unique_address_data.info())
        print(unique_address_data.head(10))
        return unique_address_data

    def get_lat_lon(self, data_frame):
        total_addresses = len(data_frame)
        error_count = 0
        error_addresses = []

        # 현재 날짜와 시간을 사용하여 폴더 생성
        current_datetime = datetime.datetime.now()
        folder_name = current_datetime.strftime('%Y%m%d_%H%M%S')
        folder_path = os.path.join(self.log_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # 결과를 CSV 파일로 저장할 경로 설정
        result_csv_path = os.path.join(folder_path, 'result.csv')

        # '위도'와 '경도' 열 추가
        data_frame['위도'] = None
        data_frame['경도'] = None

        for index, row in data_frame.iterrows():
            address = row['도로명주소']
            apiurl = "https://api.vworld.kr/req/address?"
            params = {
                "service": "address",
                "request": "getcoord",
                "crs": "epsg:4326",
                "address": address,
                "format": "json",
                "type": "road",
                "key": self.api_key
            }
            response = requests.get(apiurl, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['response']['status'] == 'OK':
                    lon = data['response']['result']['point'].get('x')
                    lat = data['response']['result']['point'].get('y')
                    if lon is not None and lat is not None:
                        # 기존 데이터프레임에 위도와 경도 열 추가
                        data_frame.at[index, '위도'] = lat
                        data_frame.at[index, '경도'] = lon
                        print(f"[{index + 1}/{total_addresses}] 주소: {address}, 위도: {lat}, 경도: {lon}")
                    else:
                        print(f"[{index + 1}/{total_addresses}] API Error: 결과가 없습니다.")
                        error_count += 1
                        error_addresses.append(address)
                else:
                    print(f"[{index + 1}/{total_addresses}] API Error: {data['response']['status']}")
                    error_count += 1
                    error_addresses.append(address)
            else:
                print(f"[{index + 1}/{total_addresses}] API Error: {response.status_code}")
                error_count += 1
                error_addresses.append(address)

        # 결과를 DataFrame으로 변환하여 CSV 파일로 저장
        data_frame.to_csv(result_csv_path, index=False)

        # 로그 파일에 기록
        self.log_result(total_addresses, error_count, error_addresses, result_csv_path)

    def log_result(self, total_addresses, error_count, error_addresses, result_csv_path):
        # 결과를 로그 파일에 기록
        log_file_path = os.path.join(os.path.dirname(result_csv_path), 'log.txt')
        with open(log_file_path, 'w') as log_file:
            log_file.write(f"최종결과: {total_addresses}개의 데이터 수집, {error_count}개의 에러 발생\n")
            log_file.write("에러 발생한 주소:\n")
            for address in error_addresses:
                log_file.write(address + '\n')
            log_file.write(f"결과 CSV 파일 경로: {result_csv_path}\n")


    def merge_result_csvs(self):
        try:
            # 결과를 저장할 빈 데이터프레임 생성
            merged_df = pd.DataFrame()

            # DATA/lat_lon_data/ 아래의 모든 폴더 리스트
            base_dir = 'DATA/lat_lon_data/'
            date_folders = [f.path for f in os.scandir(base_dir) if f.is_dir()]

            # 각 폴더의 result.csv 파일을 읽어와 병합
            total_data_count = 0
            for folder in date_folders:
                result_csv_path = os.path.join(folder, 'result.csv')
                if os.path.exists(result_csv_path):
                    df = pd.read_csv(result_csv_path)
                    total_data_count += len(df)
                    merged_df = pd.concat([merged_df, df])

            # 중복 데이터 제거
            merged_df.drop_duplicates(inplace=True)

            # 병합된 데이터프레임을 CSV 파일로 저장
            if not merged_df.empty:
                merged_csv_path = 'DATA/lat_lon_data/total_lat_lon_data.csv'
                merged_df.to_csv(merged_csv_path, index=False)
                print(f"병합된 결과가 {merged_csv_path} 파일로 저장되었습니다.")
                print(f"총 {total_data_count}개의 데이터를 가져왔으며, 중복을 제거한 후 {len(merged_df)}개의 데이터가 남았습니다.")
            else:
                print("병합할 데이터가 없습니다.")
        except Exception as e:
            print(f"오류 발생: {e}")

    def merge_dataframes(self):
        # 데이터 불러오기
        total_data = pd.read_csv('DATA/lat_lon_data/total_lat_lon_data.csv')
        address_data = pd.read_csv('DATA/lat_lon_data/address_data.csv')

        # 중복된 도로명 주소를 기준으로 병합
        merged_data = pd.merge(total_data, address_data, on='도로명주소', how='inner', suffixes=('_total', '_address'))

        # 불필요한 열 삭제
        merged_data.drop(columns=['거래금액_total', '전용면적_total', '건축년도_total', '층_total', '아파트_total'],
                         inplace=True)

        # 열 이름 변경
        merged_data.rename(columns={'거래금액_address': '거래금액', '전용면적_address': '전용면적', '건축년도_address': '건축년도',
                                    '층_address': '층', '아파트_address': '아파트'}, inplace=True)

        # 결측치가 있는 행 삭제
        merged_data.dropna(subset=['위도', '경도'], inplace=True)

        # 결과 출력
        print("=" * 50)
        print("병합된 데이터프레임 정보:")
        print(merged_data.head())
        print(merged_data.info())
        # 결과를 CSV 파일로 저장
        merged_data.to_csv('DATA/lat_lon_data/folium_data.csv', index=False)


# 사용 예시
csv_file_path = 'DATA/org_crawling_data/total_apt_trade_data.csv'
api_key = ""
geocoder = AddressGeocoder(csv_file_path, api_key)

# 첫 번째 단계: CSV 파일에서 도로명 주소 생성하고 저장
# geocoder.create_address_csv()

# 두 번째 단계: 중복값 제거
# unique_data = geocoder.remove_duplicate_addresses()

# 세 번째 단계: 위도 경도 가져오기
# geocoder.get_lat_lon(unique_data)

# 네 번째 단계: 전체 파일 합치기
# geocoder.merge_result_csvs()

geocoder.merge_dataframes()