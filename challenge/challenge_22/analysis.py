# 挑战：Pandas处理Json文件
import json
import pandas as pd
from pandas import DataFrame
from pandas.io.json import json_normalize

def analysis(file, user_id):
    times = 0
    minutes = 0

    data_str = open(file).read()
    data_list = json.loads(data_str)
    df = json_normalize(data_list)

    df_user = df[df['user_id'] == user_id]['minutes']
    times = df_user.size
    minutes = df_user.sum()
#    print(times)
#    print(minutes)

    return times, minutes

if __name__ == '__main__':
    analysis('user_study.json', 199071) 

