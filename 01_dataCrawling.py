import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta
import time
import os

class AptTradeDataCollector:
    def __init__(self, url, service_key, start_date, end_date, area_codes, sleep_time=0.1):
        self.url = url
        self.service_key = service_key
        self.start_date = start_date
        self.end_date = end_date
        self.area_codes = area_codes
        self.sleep_time = sleep_time
        self.base_folder = 'DATA/org_crawling_data/area'
        self.initialize_directories()

    def initialize_directories(self):
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)
            print(f"폴더가 생성되었습니다: {self.base_folder}")
        else:
            print(f"폴더가 이미 존재합니다: {self.base_folder}")

    def fetch_data(self, area_code, year_month):
        params = {
            'serviceKey': self.service_key,
            'pageNo': '07_dataResult',
            'numOfRows': '1000',
            'LAWD_CD': area_code,
            'DEAL_YMD': year_month
        }
        response = requests.get(self.url, params=params)
        return response

    def parse_response(self, response):
        try:
            xml_content = response.content.decode('utf-8')
            root = ET.fromstring(xml_content)
            result_code = root.find('.//resultCode').text if root.find('.//resultCode') is not None else ''
            result_msg = root.find('.//resultMsg').text
            items = root.findall('.//item')
            return result_code, result_msg, items
        except ET.ParseError as e:
            return None, f"데이터 파싱 에러: {e}", None

    def extract_data_from_items(self, items, area_name):
        rows = []
        for item in items:
            row = {
                '거래금액': item.find('.//거래금액').text.strip() if item.find('.//거래금액') is not None else '',
                '전용면적': item.find('.//전용면적').text.strip() if item.find('.//전용면적') is not None else '',
                '건축년도': item.find('.//건축년도').text.strip() if item.find('.//건축년도') is not None else '',
                '층': item.find('.//층').text.strip() if item.find('.//층') is not None else '',
                '아파트': item.find('.//아파트').text.strip() if item.find('.//아파트') is not None else '',
                '법정동': item.find('.//법정동').text.strip() if item.find('.//법정동') is not None else '',
                '지번': item.find('.//지번').text.strip() if item.find('.//지번') is not None else '',
                '년': item.find('.//년').text.strip() if item.find('.//년') is not None else '',
                '월': item.find('.//월').text.strip() if item.find('.//월') is not None else '',
                '일': item.find('.//일').text.strip() if item.find('.//일') is not None else '',
                '도로명': item.find('.//도로명').text.strip() if item.find('.//도로명') is not None else '',
                '도로명건물본번호코드': item.find('.//도로명건물본번호코드').text.strip() if item.find('.//도로명건물본번호코드') is not None else '',
                '도로명건물부번호코드': item.find('.//도로명건물부번호코드').text.strip() if item.find('.//도로명건물부번호코드') is not None else '',
                '법정동본번코드': item.find('.//법정동본번코드').text.strip() if item.find('.//법정동본번코드') is not None else '',
                '법정동부번코드': item.find('.//법정동부번코드').text.strip() if item.find('.//법정동부번코드') is not None else '',
                '법정동시군구코드': item.find('.//법정동시군구코드').text.strip() if item.find('.//법정동시군구코드') is not None else '',
                '법정동읍면동코드': item.find('.//법정동읍면동코드').text.strip() if item.find('.//법정동읍면동코드') is not None else '',
                '법정동지번코드': item.find('.//법정동지번코드').text.strip() if item.find('.//법정동지번코드') is not None else '',
                '지역': area_name  # 지역 컬럼 추가
            }
            rows.append(row)
        return rows

    def collect_apt_trade_data(self):
        total_months = (self.end_date.year - self.start_date.year) * 12 + self.end_date.month - self.start_date.month + 1
        data_collection_results = {}
        total_data = []

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        collection_folder = os.path.join(self.base_folder, timestamp)
        os.makedirs(collection_folder, exist_ok=True)

        for area_index, (area_name, area_code) in enumerate(self.area_codes.items(), start=1):
            print("="*110)
            area_name_display = f"{area_name} 전체" if len(area_name) == 2 else area_name
            print(f"수집 중인 지역: {area_name_display} ({area_code})")

            df_list = []
            current_date = self.start_date
            current_step = 0
            collected_months = 0
            error_month = None

            while current_date <= self.end_date:
                year_month = current_date.strftime('%Y%m')
                display_date = current_date.strftime('%Y년 %m월')
                response = self.fetch_data(area_code, year_month)

                if response.status_code == 200:
                    result_code, result_msg, items = self.parse_response(response)
                    if result_code == "00":
                        df_list.extend(self.extract_data_from_items(items, area_name))
                        print(f"[{current_step + 1}/{total_months}/{area_name_display}] - {display_date} 데이터 수집 완료")
                        collected_months += 1
                    else:
                        print(f"[{current_step + 1}/{total_months}/{area_name_display}] - {display_date} 데이터 요청 실패: {result_msg} (코드: {result_code})")
                        if result_code in ["10", "30", "22", "99"]:
                            error_month = display_date
                            break
                else:
                    print(f"[{current_step + 1}/{total_months}/{area_name_display}] - {display_date} HTTP 요청 실패: 상태 코드 {response.status_code}")

                current_date += timedelta(days=32)
                current_date = current_date.replace(day=1)
                time.sleep(self.sleep_time)
                current_step += 1

            result = f"{self.start_date.year}년 {self.start_date.month}월 ~ {current_date.year}년 {current_date.month}월 / {collected_months}개월 {len(df_list)}개(파싱된 데이터 수) 수집 완료"
            if error_month:
                result += f" / 코드 {result_code} 에러로 {error_month}에서 중단"
            data_collection_results[area_name_display] = result

            df = pd.DataFrame(df_list)
            print("\n**********샘플 출력**********\n")
            print(df.head())
            csv_filename = f'{area_name}_apt_trade_data.csv'
            csv_path = os.path.join(collection_folder, csv_filename)
            df.to_csv(csv_path, index=False)
            print(f"{area_name} 지역 {len(df)}개 데이터 수집 완료")
            print(f"{area_name} 데이터프레임이 CSV 파일 {csv_path}로 저장되었습니다.")

            total_data.extend(df_list)

        self.save_log(data_collection_results, collection_folder, timestamp)

    def save_log(self, data_collection_results, collection_folder, timestamp):
        log_filename = f"{timestamp}_log.txt"
        log_path = os.path.join(collection_folder, log_filename)

        with open(log_path, 'w', encoding='utf-8') as log_file:
            log_file.write("\n\n" + "="*110 + "\n")
            log_file.write("============================================최종 결과===========================================================\n")
            log_file.write("="*110 + "\n")

            for area, result in data_collection_results.items():
                log_file.write(f"지역명: {area} / {result}\n")

            log_file.write("="*110 + "\n")
            log_file.write("="*110 + "\n")
            log_file.write("="*110 + "\n\n")

        print("\n\n" + "="*110)
        print("============================================최종 결과===========================================================")
        print("="*110)

        for area, result in data_collection_results.items():
            print(f"지역명: {area} / {result}")

        print("="*110)
        print("="*110)
        print("="*110 + "\n\n")

    def merge_csv_files(self, base_directory, output_filename):
        all_data_frames = []
        file_names = []

        date_folders = [os.path.join(base_directory, d) for d in os.listdir(base_directory) if
                        os.path.isdir(os.path.join(base_directory, d))]

        for date_folder in date_folders:
            all_files = [os.path.join(date_folder, f) for f in os.listdir(date_folder) if f.endswith('.csv')]

            for file in all_files:
                try:
                    df = pd.read_csv(file)
                    if df.empty:
                        continue
                    all_data_frames.append(df)
                    file_names.append(os.path.basename(file).split('_')[0])
                except pd.errors.EmptyDataError:
                    print(f"{file} 파일은 비어있어 건너뜁니다.")

        if all_data_frames:
            merged_df = pd.concat(all_data_frames, ignore_index=True).drop_duplicates()

            # 중복 제거 전 데이터 수
            total_data_count_before = sum(df.shape[0] for df in all_data_frames)
            # 중복 제거 후 데이터 수
            total_data_count_after = merged_df.shape[0]

            merged_df.to_csv(output_filename, index=False)
            print("=" * 110)
            print(
                f"중복 데이터 {total_data_count_before - total_data_count_after}개 제거 후 {total_data_count_after}개의 데이터 수집되었습니다.")
            print(f"통합 데이터프레임이 CSV 파일 {output_filename}로 저장되었습니다.")
        else:
            print("병합할 데이터가 없습니다. CSV 파일이 생성되지 않았습니다.")

# 실행 부분
start_date = datetime(2000, 1, 1)
end_date = datetime(2023, 12, 31)
area_codes = {
    # '화성': '41590',
    # '용인 기흥': '41463',
    # '용인 수지': '41465',
    # '용인 처인': '41461',
    # '오산': '41370'
    #
    '수원 권선': '41113',
    '수원 영통': '41117',
    '수원 장안': '41111',
    '수원 팔달': '41115',
    '성남 분당': '41135',
    '성남 수정': '41131',
    '성남 중원': '41133',
    '평택': '41220'
    }
url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
service_key = ''

collector = AptTradeDataCollector(url, service_key, start_date, end_date, area_codes, sleep_time=0.1)
collector.collect_apt_trade_data()
collector.merge_csv_files('DATA/org_crawling_data/area', 'DATA/org_crawling_data/total_apt_trade_data.csv')
