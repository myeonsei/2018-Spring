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
        df[yr]=raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==gender)].groupby([dist])[status].mean()
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
            df[2*yr]=raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==0) & (raw_data[status]==1)].groupby([dist])[wage].mean()
            df[2*yr+1]=raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==1) & (raw_data[status]==1)].groupby([dist])[wage].mean()
            df[yr]=df[2*yr+1]/df[2*yr]
            del(df[2*yr]); del(df[2*yr+1])
        else:
            raw_data[dist] = raw_data[dist].apply(lambda x: x//100) # 시도 단위 레벨로 변환
            df[2*yr]=raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==0) & (raw_data[wage]<=1000) & (raw_data[status]==1)].groupby([dist])[wage].mean()
            df[2*yr+1]=raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==1) & (raw_data[wage]<=1000) & (raw_data[status]==1)].groupby([dist])[wage].mean()
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
    yr=2006
    raw_data = importing_data(dirr, codes, yr)
    dist, sex, age, marriage, industry, job, wage, status = codes[yr]
    raw_data[industry] = raw_data[industry].apply(lambda x: x//100)
    cnt = raw_data[(raw_data[sex]==gender) & (raw_data[age]>=20) & (raw_data[age]<=39) & (raw_data[status]==11)].groupby([dist, industry]).groups
    for dis in (11, 21, 22, 23, 24, 25, 26, 31, 32, 33, 34, 35, 36, 37, 38, 39):
        denom = 0
        for ind in range(10):
            if (dis, ind) in cnt:
                cnt[(dis, ind)] = len(cnt[dis, ind])
            else:
                cnt[(dis,ind)] = 0
            denom += cnt[dis, ind]
        for ind in range(10):
            cnt[dis, ind] = cnt[dis, ind] / denom
    
    for yr in range(yr_s, yr_f+1): # 해당 연도에 대해 산업별 평균 임금 산정 및 곱해서 outcome까지
        raw_data = importing_data(dirr, codes, yr)
        dist, sex, age, marriage, industry, job, wage, status = codes[yr]
        av_inc = {}
        
        if yr == 2006 or yr == 2007:
            raw_data[wage] = raw_data[wage].apply(lambda x: ad0607[x] if x in ad0607 else 0)
            raw_data[status] = raw_data[status].apply(lambda x: 0 if x != 11 else 1)
            raw_data[industry] = raw_data[industry].apply(lambda x: x//100)
            av_inc = raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==gender) & (raw_data[status]==1)].groupby([industry])[wage].mean()

        else:
            raw_data[industry] = raw_data[industry].apply(lambda x: x//10)
            raw_data[dist] = raw_data[dist].apply(lambda x: x//100)
            av_inc = raw_data[(raw_data[age]>=age_l) & (raw_data[age]<=age_u) & (raw_data[sex]==gender) & (raw_data[wage]<=1000) & (raw_data[status]==1)].groupby([industry])[wage].mean()

        for dis in (11, 21, 22, 23, 24, 25, 26, 31, 32, 33, 34, 35, 36, 37, 38, 39):
            dis_inc = 0
            for ind in range(10):
                dis_inc += cnt[dis, ind] * av_inc[ind]
            df.loc[dis, yr] = dis_inc       
            
    return df

#return_unemp(dirr, codes).to_csv(dirr+'unemp.csv', encoding='utf-8')
