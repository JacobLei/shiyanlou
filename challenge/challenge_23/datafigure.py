import json
import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt
from pandas import DataFrame
from pandas.io.json import json_normalize

def data(file):

    data_str = open(file).read()
    data_list = json.loads(data_str)
    df = json_normalize(data_list)
    id_minutes = df[['user_id', 'minutes']].groupby('user_id').sum()

    return id_minutes

def data_plot():

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title("StudyData")
    ax.set_ylabel("Study Time")
    ax.set_xlabel("User ID")
    
    x_ticks = np.arange(0, 250000, 50000)
    y_ticks = np.arange(0, 3500, 500)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    id_minutes = data('user_study.json')
    x = id_minutes.index
    y = id_minutes['minutes']
    plt.plot(x, y)

#    id_minutes.plot()
    plt.show()




if __name__ == '__main__':
#     data('user_study.json')
    data_plot()
