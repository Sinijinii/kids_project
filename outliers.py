## zscore구현을 위한 라이브러리
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager, rc
from pandas import Series, DataFrame
font_name = font_manager.FontProperties(fname = "C:/Windows/Fonts/malgun.ttf").get_name( )
rc('font', family = font_name)
matplotlib.rcParams['axes.unicode_minus'] = False

#데이터불러오기
all=pd.read_csv('C:/Users/AICTTechPlan04/Desktop/신희진/DB/kids_data.csv',sep = ",",encoding="CP949")

import scipy.stats as ss
# 각개인별 zscore값 구하기
roa=all.loc[all['Name']=="이로아"]# 이름만 따로 변경(for문 사용해서 한번에도 가능)
#Zscore값
roa['Zscore']=ss.zscore(roa['HeartRate'])

#modi_Zscore값 구하는 함수
def modi_zscore(data):
    median_data = np.median(data)
    mad=np.median(data.map(lambda x: np.abs(x-median_data)))
    modified_z_score = data.map(lambda x: 0.6745*(x-median_data)/mad)
    data["modi_zscore"]=data.map(lambda x: 0.6745*(x-median_data)/mad)
    return data
#modi_Zscore값 저장
roa['midi_zsc']=modi_zscore(roa['Zscore'])
roa['midi_zsc']=roa['midi_zsc'].astype(float)
#roa['midi_zsc']의 값으로 초기 기준설정
a =min(roa.loc[roa['midi_zsc']>=1.5]['midi_zsc'])
Be_pl=roa['HeartRate'][roa.loc[roa['midi_zsc']==a].index]
a =min(roa.loc[roa['midi_zsc']>=2]['midi_zsc'])
Wa_pl=roa['HeartRate'][roa.loc[roa['midi_zsc']==a].index]
a =max(roa.loc[roa['midi_zsc']>=2]['midi_zsc'])
dan_pl=roa['HeartRate'][roa.loc[roa['midi_zsc']==a].index]
a =max(roa.loc[roa['midi_zsc']<=-1.5]['midi_zsc'])
Be_mi=roa['HeartRate'][roa.loc[roa['midi_zsc']==a].index]
a =max(roa.loc[roa['midi_zsc']<=-2]['midi_zsc'])
Wa_mi=roa['HeartRate'][roa.loc[roa['midi_zsc']==a].index]
a =min(roa.loc[roa['midi_zsc']<=-2]['midi_zsc'])
dan_mi=roa['HeartRate'][roa.loc[roa['midi_zsc']==a].index]
print("관심단계기준:",Be_mi,Be_pl)
print("주의단계기준:",Wa_mi,Wa_pl)
print("위험단계기준:",dan_mi,dan_pl)



#or 다른 방법의 기준
#interquantile_range
# 관심단계
def get_lower_upper_Beware(data):
    data1 = np.percentile(data, 35) # 하위 35
    data2 = np.percentile(data, 65) # 상위 35
    interquantile_range = data2-data1
    lower_bound = data1 - (interquantile_range*1.2) # 1.2배가 넘어서는걸을 이상치로 판단
    upper_bound = data2 + (interquantile_range*1.2)
    return lower_bound, upper_bound
get_lower_upper_Beware(roa['HeartRate'])
print("관심단계기준 : ",get_lower_upper_Beware(roa['HeartRate']))
# 주의단계
def get_lower_upper_Warning(data):
    data1 = np.percentile(data, 20) # 하위 20
    data2 = np.percentile(data, 80) # 상위 20
    interquantile_range = data2-data1
    lower_bound = data1 - (interquantile_range*1.2) # 1.2배가 넘어서는걸을 이상치로 판단
    upper_bound = data2 + (interquantile_range*1.2)
    return lower_bound, upper_bound
get_lower_upper_Warning(roa['HeartRate'])
print("주의단계기준 : ",get_lower_upper_Warning(roa['HeartRate']))
# 위험단계
def get_lower_upper_danger(data):
    data1 = np.percentile(data, 10) # 하위 10
    data2 = np.percentile(data, 90) # 상위 10
    interquantile_range = data2-data1
    lower_bound = data1 - (interquantile_range*1.2) # 1.2배가 넘어서는걸을 이상치로 판단
    upper_bound = data2 + (interquantile_range*1.2)
    return lower_bound, upper_bound
get_lower_upper_danger(roa['HeartRate'])
print("위험단계기준 : ",get_lower_upper_danger(roa['HeartRate']))
