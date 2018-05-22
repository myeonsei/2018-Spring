import numpy as np; import pandas as pd; from os import listdir
pdir = 'C:\\Users\\myeon\\Desktop\\응용 계량경제학\\팀플\\KLIPS\\personal\\'
hdir = 'C:\\Users\\myeon\\Desktop\\응용 계량경제학\\팀플\\KLIPS\\household\\'
fulldata = pd.DataFrame([], columns = ['ID', 'HHID', 'SEX', 'AGE', 'REGULAR', 'EDU', 'WORKINGHOURS', 'EXTRAWORKING', 'WAGE', 'MARRIAGE', 'STATUS', 'FULLTIME', 'YEAR', 'SPWK', 'SPWT', 'CHILDREN'])
yrs = list(range(1,20))
yrs.remove(2); yrs.remove(3) # 2에는 

for y in yrs:
    if y<10:
        strnum = '0'+str(y)
    else:
        strnum = str(y)
    print(y)
    data = pd.read_csv(pdir+str(y)+'.csv', engine='python')
    data['id'] = data.iloc[:,0]
    df = data[(data['p'+strnum+'1642']>0) & ((data['p'+strnum+'0102']==10) | (data['p'+strnum+'0102']==20))][['id', 'hhid'+strnum, 'p'+strnum+'0101', 'p'+strnum+'0107', 'p'+strnum+'0317', 'p'+strnum+'0110', 'p'+strnum+'1006', 'p'+strnum+'1012',\
             'p'+strnum+'1642', 'p'+strnum+'5501', 'p'+strnum+'0102']].fillna(0) #ID, HHID, SEX, AGE, REGULAR, EDU, WORKINGHOURS, WAGE, MARRIAGE
    del(data)
    df.columns = ['ID', 'HHID', 'SEX', 'AGE', 'REGULAR', 'EDU', 'WORKINGHOURS', 'EXTRAWORKING', 'WAGE', 'MARRIAGE', 'STATUS']
    df['FULLTIME'] = df['WORKINGHOURS'] + df['EXTRAWORKING']
    df['YEAR'] = y
    idx = df.groupby(['HHID']).groups
    df['SPWK']=0; df['SPWT'] = 0 #; couple = []
    for i in idx.keys():
        if len(idx[i]) > 1:
            df.loc[idx[i], 'SPWK'] = 1
            df.loc[idx[i][0], 'SPWT'] = df.loc[idx[i][1], 'FULLTIME']; df.loc[idx[i][1], 'SPWT'] = df.loc[idx[i][0], 'FULLTIME']
    hhdata = pd.read_csv(hdir+str(y)+'h.csv', engine='python', index_col='hhid'+strnum)
    df['CHILDREN'] = list(hhdata.loc[df['HHID'], 'h'+strnum+'1502'])
    del(hhdata)
    fulldata=fulldata.append(df, ignore_index=True)
    del(df)
fulldata.to_csv('C:\\Users\\myeon\\Desktop\\응용 계량경제학\\팀플\\KLIPS\\trimmed.csv', encoding='utf-8')
del(fulldata)

## Extra Features ###

import pandas as pd

df = pd.read_csv('C:\\Users\\myeon\\Desktop\\응용 계량경제학\\팀플\\KLIPS\\trimmed.csv', engine = 'python', index_col=0)
df = df[df['FULLTIME']>0]
df = df.fillna(0)
for i in df.index:
    if df.loc[i, 'SPWK'] == 1 and df.loc[i, 'SPWT'] == 0: df.loc[i, 'SPWT'] = None
df.to_csv('C:\\Users\\myeon\\Desktop\\응용 계량경제학\\팀플\\KLIPS\\trimmed.csv', encoding='utf-8')
