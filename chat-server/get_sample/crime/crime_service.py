import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from context.model.crime_model import CrimeModel
from icecream import ic
from crime.crime_util import Reader
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
'''
문제정의 !
서울시의 범죄현황과 CCTV현황을 분석해서
정해진 예산안에서 구별로 다음해에 배분하는 기준을 마련하시오.
예산금액을 입력하면, 구당 할당되는 CCTV 카운터를 자동으로
알려주는 AI 프로그램을 작성하시오.
'''

class CrimeService:
    def __init__(self):
        self.data = CrimeModel()
        self.data.dname = './crime/data/'
        self.data.sname = './crime/save/'
        self.data.fname = 'crime_in_seoul.csv'
        self.data.fname2 = 'cctv_in_seoul.csv' #cctv
        self.crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인 발생', '강도 발생', '강간 발생', '절도 발생', '폭력 발생']
        self.arrest_columns = ['살인 검거', '강도 검거' ,'강간 검거', '절도 검거','폭력 검거']

    def crime_dataframe(self) -> pd.DataFrame:
        return pd.read_csv(f'{self.data.dname}{self.data.fname}', encoding='UTF-8', thousands=',')
    
    def cctv_dataframe(self) -> pd.DataFrame:
        return pd.read_csv(f'{self.data.dname}{self.data.fname2}', encoding='UTF-8', thousands=',')

    def save_model(self, fname, dfname:pd.DataFrame) -> pd.DataFrame:
        return dfname.to_csv(f'{self.data.sname}{fname}', sep=',', na_rep="NaN")
    
    def save_police_position(self) -> None:
        station_names = []
        crime = self.crime_dataframe()
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1]) + '경찰서')
        station_addreess = []
        station_lats = []
        station_lngs = []
        reader = Reader()
        gmaps = reader.gmaps(os.environ["api_key"])
        for name in station_names:
            t = gmaps.geocode(name, language='ko')
            print(t)
            station_addreess.append(t[0].get("formatted_address"))
            t_loc = t[0].get("geometry")
            station_lats.append(t_loc['location']['lat'])
            station_lngs.append(t_loc['location']['lng'])
        
        gu_names = []
        for name in station_addreess:
            tmp = name.split()
            gu_name = [gu for gu in tmp if gu[-1] == '구'][0]
            gu_names.append(gu_name)
        
        crime['구별'] = gu_names
        # 구 와 경찰서의 위치가 다른 경우 수작업
        crime.loc[crime['관서명'] == '혜화서', ['구별']] = '종로구'
        crime.loc[crime['관서명'] == '서부서', ['구별']] = '은평구'
        crime.loc[crime['관서명'] == '강서서', ['구별']] = '양천구'
        crime.loc[crime['관서명'] == '종암서', ['구별']] = '성북구'
        crime.loc[crime['관서명'] == '방배서', ['구별']] = '서초구'
        crime.loc[crime['관서명'] == '수서서', ['구별']] = '강남구'
        crime.to_csv(f'{self.data.sname}police_position.csv')


    
if __name__ == "__main__":
    service = CrimeService()
    crime_df = service.crime_dataframe()
    cctv_df = service.cctv_dataframe()
    # print(crime_df)
    # print(cctv_df)
    service.save_police_position()