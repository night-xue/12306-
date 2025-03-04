import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from datetime import datetime,timedelta

def get_time(data):
    num = list(data['车次'])
    start_time = list(data['出发时间'])
    end_time = list(data['到达时间'])

    plt.figure(dpi=128,figsize=(5,5))
    plt.plot(num, start_time, label='出发时间', ls='--', lw='0.5')
    plt.scatter(num, start_time, marker='v', s=15)
    plt.plot(num, end_time, label='到达时间', ls='--', lw='0.5')
    plt.scatter(num, end_time, marker='^', s=15)

    plt.legend()

    plt.xticks(num,fontsize=8,rotation=45)
    plt.yticks(fontsize=8)
    plt.title('起止时间')
    plt.xlabel('车次')
    plt.ylabel('时间')
    plt.show()


# def get_use_time(data):
#     num = list(data['车次'])
#     use_time = list(data['耗时'])
#     use_max = max(use_time)
#     use_max_num = num[use_time.index(use_max)]
#     use_min = min(use_time)
#     use_min_num = num[use_time.index(use_min)]
#
#
#     plt.figure(dpi=128,figsize=(5,5))
#     plt.bar(num,use_time)
#
#     plt.text(use_max_num, use_max, str(use_max), ha='center', va='bottom', fontsize=10.5)
#     plt.text(use_min_num, use_min, str(use_min), ha='center', va='bottom', fontsize=10.5)
#
#     plt.xticks(num, fontsize=8, rotation=45)
#
#     plt.yticks(use_time, fontsize=8)
#     plt.title('火车运行时间')
#     plt.xlabel('车次')
#     plt.ylabel('耗时/h')
#     plt.show()

def main():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题
    # plt.rcParams['anumes.unicode_minus'] = False  # 解决负号显示问题
    data = pd.read_csv('data.csv',encoding='gbk')
    print(data)
    get_time(data)
    # get_use_time(data)
if __name__ == '__main__':
    main()