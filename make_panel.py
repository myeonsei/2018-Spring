import numpy as np; import pandas as pd; from os import listdir
dirr = 'C:\\test' # 새로 지정해주기 -
files = listdir(dirr)

def make_frame(dirr, files, yr_s=2006, yr_f=2017):
    data = pd.read_csv(dirr + '\\' + files[0], engine = 'python')
    ids = data.iloc[:,0].values
    hei = len(data)
    wid = yr_f - yr_s + 1
    full_len = hei * wid
    return [pd.DataFrame(index = range(full_len)), ids, hei, wid]

make_frame(dirr, files)

def return_panel(dirr, files, yr_s=2006, yr_f=2017):
    df, ids, hei, wid = make_frame(dirr, files)
    idx = []
    for i in range(hei):
        idx.extend([ids[i]]*wid)
    df['id'] = idx
    df['year'] = list(range(yr_s, yr_f+1)) * hei

    for i in files:
        df[i[:10]] = np.array(pd.read_csv(dirr + '\\' + i, engine = 'python').iloc[:,1:]).reshape(hei*wid)
        
    return df
    
return_panel(dirr, files)
