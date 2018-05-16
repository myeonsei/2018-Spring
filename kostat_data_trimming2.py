## 지역별 고용조사 2 for 교육 연한 ##
import pandas as pd

dist, sex, age, educ, grad = range(5) # 코드 번호
educ2007 = {0 :0, 11:6, 12:3, 12:3, 13:3, 14:3, 15:6,\
21:9, 22:7.5, 23:7.5, 24:7.5, 25:9,\
31:12, 32:10.5, 33:10.5, 34:10.5, 35:12,\
41:14, 42:13, 43:13, 44:13, 45:14,\
51:16, 52:14, 53:14, 54:14, 55:16,\
61:19, 62:17.5, 63:17.5, 64:17.5, 65:19}
educ2008 = {0 :0, 11:6, 12:3, 12:3, 13:3, 14:3,\
21:9, 22:7.5, 23:7.5, 24:7.5,\
31:12, 32:10.5, 33:10.5, 34:10.5,\
41:14, 42:13, 43:13, 44:13,\
51:16, 52:14, 53:14, 54:14,\
61:18, 62:17, 63:17, 64:17,\
71:21, 72:19.5,  73:19.5,  74:19.5}
dirr = 'C:\\Users\\myeon\\Desktop\\인구와 경제\\팀플 관련\\Data\\지역별 고용조사2\\'

def make_frame(dirr, importing_data2, code=0, yr_s=2006, yr_f=2017): # 범용
    idx=set([])
    for i in range(yr_s, yr_f+1):
        d = importing_data2(dirr, i)
        c = code     
        print(i, set(d[c]))
        idx = set(d[c]) | idx
        print(i)
    idx = sorted(idx)
    return pd.DataFrame(index = idx)

def importing_data2(dirr, year):
    raw_data = pd.read_csv(dirr + str(year) + '.csv', engine='python', header = None)
    raw_data[educ] = 10*raw_data[educ] + raw_data[grad] 
    raw_data[sex] = raw_data[sex].apply(lambda x: x-1)

    if year <= 2007:
        raw_data.loc[0,0] = 11 # 데이터 파일 이상으로 필요한 부분
        raw_data[dist] = raw_data[dist].apply(int)
        raw_data[educ]=raw_data[educ].apply(lambda x: educ2007[x] if x in educ2007 else 0)
    elif year >= 2008:
        raw_data.loc[0,0] = 1100 # 동일한 이유로
        raw_data[dist] = raw_data[dist].apply(int)
        raw_data[dist] = raw_data[dist].apply(lambda x: x//100) # 시도 단위 변환
        raw_data[educ]=raw_data[educ].apply(lambda x: educ2008[x] if x in educ2008 else 0)

    return raw_data

def return_educ(dirr, gender, age_l = 20, age_u = 39, yr_s=2006, yr_f=2017): # 남자 0 여자 1임.
    df = make_frame(dirr, importing_data2)
    for yr in range(yr_s, yr_f+1):
        raw_data = importing_data2(dirr, yr)
        df[yr]=raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==gender)].groupby([dist])[educ].mean()
    return df

return_educ(dirr,0).to_csv(dirr+'menprovince.csv', encoding='utf-8')
return_educ(dirr,1).to_csv(dirr+'womenprovince.csv', encoding='utf-8')
