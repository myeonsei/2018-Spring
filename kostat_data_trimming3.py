## Panel Data Return

import numpy as np; import pandas as pd; from os import listdir
dirr = 'C:\\test' # 새로 지정해주기 -
files = listdir(dirr)

def make_frame(dirr, files, yr_s=2006, yr_f=2017):
    data = pd.read_csv(dirr + '\\' + files[0], engine = 'python')
    ids = data.iloc[:,0].values[:16]
    hei = len(ids)
    wid = yr_f - yr_s + 1
    full_len = hei * wid
    return [pd.DataFrame(index = range(full_len)), ids, hei, wid]

def return_panel(dirr, files, yr_s=2006, yr_f=2017):
    df, ids, hei, wid = make_frame(dirr, files)
    idx = []
    for i in range(hei):
        idx.extend([ids[i]]*wid)
    df['id'] = idx
    df['year'] = list(range(yr_s, yr_f+1)) * hei

    for i in files:
        print(i)
        df[i[:10]] = np.array(pd.read_csv(dirr + '\\' + i, engine = 'python').iloc[:16,1:]).reshape(hei*wid)
        
    return df

return_panel(dirr, files).to_csv('C:\\test\\광역new.csv', encoding = 'utf-8')

## 교수님 의견 수렴한 새로운 데이터 Return

import pandas as pd

def make_frame(dirr, codes, code, importing_data, yr_s=2006, yr_f=2017): # 범용
    idx=set([])
    for i in range(yr_s, yr_f+1):
        d = importing_data(dirr, codes, i)
        c = codes[i][code]
        idx = set(d[c]) | idx
    idx = sorted(idx)
    return pd.DataFrame(index = idx)

def import_data(dirr, year):
    raw_data = pd.read_csv(dirr + str(year) + '.txt', engine='python', header = None)
    return raw_data

########## 지역별 고용조사 1 ##########

dirr = 'C:\\Users\\myeon\\Desktop\\인구와 경제\\팀플 관련\\Data\\지역별 고용조사\\'
codes = {2017: tuple(range(8)), 
              2016: tuple(range(8)),
              2015: tuple(range(8)),
              2014: tuple(range(8)),
              2013: tuple(range(8)),
              2012: tuple(range(8)),
              2011: tuple(range(8)),
              2010: tuple(range(8)),
              2009: tuple(range(8)),
              2008: tuple(range(8)),
              2007: (0,1,2,3,5,6,4,7),
              2006: tuple(range(8))} # 순번 매기기

def importing_data(dirr, codes, year):
    raw_data = pd.read_csv(dirr + str(year) + '.txt', engine='python', header = None)
    dist, sex, age, marriage, industry, job, wage, status = codes[year]
    raw_data[sex] = raw_data[sex].apply(lambda x: x-1)
    raw_data[marriage] = raw_data[marriage].apply(lambda x: 1 if x==2 or x==3 else 0)
    return raw_data

def return_marriage(dirr, codes, age_l = 20, age_u = 39, yr_s=2006, yr_f=2017):
    df = make_frame(dirr, codes, 0, importing_data)
    for yr in range(yr_s, yr_f+1):
        raw_data = importing_data(dirr, codes, yr)
        dist, sex, age, marriage, industry, job, wage, status = codes[yr]
        if yr >= 2008: # 시도 단위 레벨로 변환
            raw_data[dist] = raw_data[dist].apply(lambda x: x//100) 
        df[yr]=raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==1)].groupby([dist])[marriage].mean()
    return df

def return_emp(dirr, codes, gender, age_l = 20, age_u = 39, yr_s=2006, yr_f=2017): # 남자 0 여자 1임.
    df = make_frame(dirr, codes, 0, importing_data)
    for yr in range(yr_s, yr_f+1):
        raw_data = importing_data(dirr, codes, yr)
        dist, sex, age, marriage, industry, job, wage, status = codes[yr]
        if yr == 2006 or yr == 2007:
            raw_data[status] = raw_data[status].apply(lambda x: 0 if x != 11 else 1)
        else:
            raw_data[status] = raw_data[status].apply(lambda x: 0 if x != 1 else 1)
            raw_data[dist] = raw_data[dist].apply(lambda x: x//100) # 시도 단위 레벨로 변환
        df[yr]=raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==gender) & (raw_data[marriage]==0)].groupby([dist])[status].mean()
    return df
 
def return_raw_wage_diff(dirr, codes, age_l = 20, age_u = 39, yr_s=2006, yr_f=2017): # 남자 0 여자 1임.
    df = make_frame(dirr, codes, 0, importing_data)
    ad0607 = {1: 25, 2: 75, 3: 125, 4: 175, 5:225, 6:275, 7:350, 8:450, 9:550, 10:800}
    for yr in range(yr_s, yr_f+1):
        raw_data = importing_data(dirr, codes, yr)
        dist, sex, age, marriage, industry, job, wage, status = codes[yr]
        if yr == 2006 or yr == 2007:
            raw_data[wage] = raw_data[wage].apply(lambda x: ad0607[x] if x in ad0607 else 0)
            raw_data[status] = raw_data[status].apply(lambda x: 0 if x != 11 else 1)
            df[2*yr]=raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==0) & (raw_data[status]==1) & (raw_data[marriage]==0)].groupby([dist])[wage].mean()
            df[2*yr+1]=raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==1) & (raw_data[status]==1) & (raw_data[marriage]==0)].groupby([dist])[wage].mean()
            df[yr]=df[2*yr+1]/df[2*yr]
            del(df[2*yr]); del(df[2*yr+1])
        else:
            raw_data[dist] = raw_data[dist].apply(lambda x: x//100) # 시도 단위 레벨로 변환
            df[2*yr]=raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==0) & (raw_data[wage]<=1000) & (raw_data[status]==1) & (raw_data[marriage]==0)].groupby([dist])[wage].mean()
            df[2*yr+1]=raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==1) & (raw_data[wage]<=1000) & (raw_data[status]==1) & (raw_data[marriage]==0)].groupby([dist])[wage].mean()
            df[yr]=df[2*yr+1]/df[2*yr]
            del(df[2*yr]); del(df[2*yr+1])
        
    return df

def return_unemp(dirr, codes, age_l = 20, age_u = 39, yr_s=2006, yr_f=2017): 
    df = make_frame(dirr, codes, 0, importing_data)
    for yr in range(yr_s, yr_f+1):
        raw_data = importing_data(dirr, codes, yr)
        dist, sex, age, marriage, industry, job, wage, status = codes[yr]
        if yr >= 2008: # 시도 단위 레벨로 변환
            raw_data[dist] = raw_data[dist].apply(lambda x: x//100) 
        idx = raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u)].groupby([dist]).groups
        if yr == 2006 or yr == 2007:
            for i in idx.keys():
                cnt=pd.value_counts(raw_data.loc[idx[i],7])
                a=cnt[11]/(cnt[11]+cnt[12]) if 12 in cnt.keys() else 1
                df.loc[i,yr]=a
        else:
            for i in idx.keys():
                cnt=pd.value_counts(raw_data.loc[idx[i],7])
                a=cnt[1]/(cnt[1]+cnt[2]) if 2 in cnt.keys() else 1
                df.loc[i,yr]=a
    return df

def return_bartik(dirr, codes, gender, age_l = 20, age_u = 39, yr_s=2006, yr_f=2017): # 남자 0 여자 1임.
    df = make_frame(dirr, codes, 0, importing_data)
    ad0607 = {1: 25, 2: 75, 3: 125, 4: 175, 5:225, 6:275, 7:350, 8:450, 9:550, 10:800}

    # 06년도 기준 산업 비율 만들기 -> 완료
#     yr=2006
#     raw_data = importing_data(dirr, codes, yr)
#     dist, sex, age, marriage, industry, job, wage, status = codes[yr]
#    raw_data[industry] = raw_data[industry].apply(lambda x: x//100)

    
    for yr in range(yr_s, yr_f+1): # 해당 연도에 대해 산업별 평균 임금 산정 및 곱해서 outcome까지
        raw_data = importing_data(dirr, codes, yr)
        dist, sex, age, marriage, industry, job, wage, status = codes[yr]
        av_inc = {}
        
        if yr == 2006 or yr == 2007:
            raw_data[wage] = raw_data[wage].apply(lambda x: ad0607[x] if x in ad0607 else 0)
            raw_data[status] = raw_data[status].apply(lambda x: 0 if x != 11 else 1)
            raw_data[industry] = raw_data[industry].apply(lambda x: x//100)
            av_inc = raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==gender) & (raw_data[status]==1) & (raw_data[marriage]==0)].groupby([dist, industry])[wage].mean()

        else:
            raw_data[industry] = raw_data[industry].apply(lambda x: x//10)
            raw_data[dist] = raw_data[dist].apply(lambda x: x//100)
            av_inc = raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==gender) & (raw_data[wage]<=1000) & (raw_data[status]==1) & (raw_data[marriage]==0)].groupby([dist, industry])[wage].mean()

        cnt = raw_data[(raw_data[sex]==1) & (raw_data[age]>=20) & (raw_data[age]<=39) & (raw_data[status]==1) & (raw_data[marriage]==0)].groupby([industry]).groups
        del(cnt[0]) # 0 산업은 제외
        denom = 0
        for ind in range(1,10):
            if ind in cnt:
                cnt[ind] = len(cnt[ind])
            else:
                cnt[ind] = 0
            denom += cnt[ind]
        for ind in range(1,10):
            cnt[ind] = cnt[ind] / denom

        for dis in (11, 21, 22, 23, 24, 25, 26, 31, 32, 33, 34, 35, 36, 37, 38, 39):
            dis_inc = 0
            cntagg = 0
            for ind in range(1,10):
                if ind in av_inc[dis]:
                    dis_inc += cnt[ind] * av_inc[dis, ind]
                    cntagg += cnt[ind]
            df.loc[dis, yr] = dis_inc / cntagg
        print(yr)    
    return df

#dd=pd.read_csv(dirr + '2030취업률(시도+시군)_지역별고용조사.csv', engine='python', index_col=0).apply(lambda x: 1-x if x != a.empty else None)

#dd
(return_bartik(dirr, codes, 1)/return_bartik(dirr, codes, 0)).to_csv(dirr+'newbartik.csv', encoding='utf-8')
