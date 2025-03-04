import requests
from bs4 import BeautifulSoup
import csv
import json
# -*- coding: gbk -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print("成功访问")
        return r.text
    except:
        print("访问错误")
        return " "


def get_content(html):
    init = []
    bs = BeautifulSoup(html, "html.parser")
    body = bs.body
    data = body.find('div',{'id': '7d'})
    data2 = body.find_all('div', {'class':'left-div'})
    text = data2[2].find('script').string
    print(text)
    text = text[text.index('=') + 1:-2]
    jd = json.loads(text)
    dayone = jd['od']['od2']
    In_day = []
    count = 0
    for i in dayone:
        info = []
        if count <= 23:
            info.append(i['od21'])  # 时间
            info.append(i['od22'])  # 温度
            info.append(i['od24'])  # 风力方向
            info.append(i['od25'])  # 风级
            info.append(i['od26'])  # 降水量
            info.append(i['od27'])  # 相对湿度
            info.append(i['od28'])  # 空气质量
            # print(info)
            In_day.append(info)
        count = count + 1
    # 下面获取7天的数据
    ul = data.find('ul')  # 找到所有的ul标签
    li = ul.find_all('li')  # 找到左右的li标签
    i = 0  # 控制获取的天数
    for day in li:  # 遍历找到的每一个li
        if i > 0 and i < 7:
            info = []  # 临时存放每天的数据
            date = day.find('h1').string  # 得到日期
            date = date[0:date.index('日')]  # 取出日期号
            info.append(date)
            inf = day.find_all('p')  # 找出li下面的p标签,提取第一个p标签的值，即天气
            info.append(inf[0].string)

            tem_low = inf[1].find('i').string  # 找到最低气温

            if inf[1].find('span') is None:  # 天气预报可能没有最高气温
                tem_high = None
            else:
                tem_high = inf[1].find('span').string  # 找到最高气温
            info.append(tem_low[:-1])
            if tem_high[-1] == '℃':
                info.append(tem_high[:-1])
            else:
                info.append(tem_high)

            wind = inf[2].find_all('span')  # 找到风向
            for j in wind:
                info.append(j['title'])

            wind_scale = inf[2].find('i').string  # 找到风级
            index1 = wind_scale.index('级')
            info.append(int(wind_scale[index1 - 1:index1]))
            init.append(info)
        i = i + 1
    return init, In_day


def get_content2(html):
    init = []
    bs = BeautifulSoup(html, "html.parser")
    body = bs.body
    data = body.find('div', {'id': '15d'})
    ul = data.find('ul')
    li = ul.find_all('li')
    i = 0
    for day in li:
        if i < 8:
            info = []
            date = day.find('span', {'class': 'time'}).string  # 得到日期
            date = date[date.index('（') + 1:-2]  # 取出日期号
            info.append(date)
            weather = day.find('span', {'class': 'wea'}).string  # 找到天气
            info.append(weather)
            tem = day.find('span', {'class': 'tem'}).text  # 找到温度
            info.append(tem[tem.index('/') + 1:-1])  # 找到最低气温
            info.append(tem[:tem.index('/') - 1])  # 找到最高气温
            wind = day.find('span', {'class': 'wind'}).string  # 找到风向
            if '转' in wind:  # 如果有风向变化
                info.append(wind[:wind.index('转')])
                info.append(wind[wind.index('转') + 1:])
            else:  # 如果没有风向变化，前后风向一致
                info.append(wind)
                info.append(wind)
            wind_scale = day.find('span', {'class': 'wind1'}).string  # 找到风级
            index1 = wind_scale.index('级')
            info.append(int(wind_scale[index1 - 1:index1]))
            init.append(info)
    return init


def write_to_csv(file_name, data, day=14):
    with open(file_name, 'w', errors='ignore', newline='') as f:
        if day == 14:
            header = ['日期', '气温', '最低气温', '最高气温', '风向1', '风向2', '风级']
        else:
            header = ['小时', '温度', '风力方向', '风级', '降水量', '相对湿度', '空气质量']
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        f_csv.writerows(data)


def tem_curve(data):
    hour = list(data['小时'])
    tem = list(data['温度'])
    for i in range(0, 24):
        if math.isnan(tem[i]) == True:
            tem[i] = tem[i - 1]
    tem_ave = sum(tem) / 24
    tem_max = max(tem)
    tem_max_hour = hour[tem.index(tem_max)]
    tem_min = min(tem)
    tem_min_hour = hour[tem.index(tem_min)]
    x = []
    y = []
    for i in range(0, 24):
        x.append(i)
        y.append(tem[hour.index(i)])
    plt.figure(1)
    plt.plot(x, y, color='#4a9de4', label='温度')
    plt.scatter(x, y, color='#3d00ff')
    plt.plot([0, 24], [tem_ave, tem_ave], c='#2d9ac1', linestyle='--', label='平均温度')
    plt.text(tem_max_hour + 0.15, tem_max + 0.15, str(tem_max), ha='center', va='bottom', fontsize=10.5)
    plt.text(tem_min_hour + 0.15, tem_min + 0.15, str(tem_min), ha='center', va='bottom', fontsize=10.5)
    plt.xticks(x)
    plt.legend()
    plt.title('一天温度变化曲线图')
    plt.xlabel('时间/h')
    plt.ylabel('摄氏度/℃')
    plt.show()


def hum_curve(data):
    hour = list(data['小时'])
    hum = list(data['相对湿度'])
    for i in range(0, 24):
        if math.isnan(hum[i]) == True:
            hum[i] = hum[i - 1]
    hum_ave = sum(hum) / 24
    hum_max = max(hum)
    hum_max_hour = hour[hum.index(hum_max)]
    hum_min = min(hum)
    hum_min_hour = hour[hum.index(hum_min)]
    x = []
    y = []
    for i in range(0, 24):
        x.append(i)
        y.append(hum[hour.index(i)])
    plt.figure(2)
    plt.plot(x, y, color='#356be6', label='相对湿度')
    plt.scatter(x, y, color='blue')
    plt.plot([0, 24], [hum_ave, hum_ave], c='#4900fc', linestyle='--', label='平均相对湿度')
    plt.text(hum_max_hour + 0.15, hum_max + 0.15, str(hum_max), ha='center', va='bottom', fontsize=10.5)
    plt.text(hum_min_hour + 0.15, hum_min + 0.15, str(hum_min), ha='center', va='bottom', fontsize=10.5)
    plt.xticks(x)
    plt.legend()
    plt.title('一天相对湿度变化曲线图')
    plt.xlabel('时间/h')
    plt.ylabel('百分比/%')
    plt.show()


def air_curve(data):
    hour = list(data['小时'])
    air = list(data['空气质量'])
    print(type(air[0]))
    for i in range(0, 24):
        if math.isnan(air[i]) == True:
            air[i] = air[i - 1]
    air_ave = sum(air) / 24
    air_max = max(air)
    air_max_hour = hour[air.index(air_max)]
    air_min = min(air)
    air_min_hour = hour[air.index(air_min)]
    x = []
    y = []
    for i in range(0, 24):
        x.append(i)
        y.append(air[hour.index(i)])
    plt.figure(3)

    for i in range(0, 24):
        if y[i] <= 50:
            plt.bar(x[i], y[i], color='lightgreen', width=0.7)  # 1等级
        elif y[i] <= 100:
            plt.bar(x[i], y[i], color='wheat', width=0.7)  # 2等级
        elif y[i] <= 150:
            plt.bar(x[i], y[i], color='orange', width=0.7)  # 3等级
        elif y[i] <= 200:
            plt.bar(x[i], y[i], color='orangered', width=0.7)  # 4等级
        elif y[i] <= 300:
            plt.bar(x[i], y[i], color='darkviolet', width=0.7)  # 5等级
        elif y[i] > 300:
            plt.bar(x[i], y[i], color='maroon', width=0.7)  # 6等级
    plt.plot([0, 24], [air_ave, air_ave], c='black', linestyle='--')
    plt.text(air_max_hour + 0.15, air_max + 0.15, str(air_max), ha='center', va='bottom', fontsize=10.5)  # 标出最高空气质量
    plt.text(air_min_hour + 0.15, air_min + 0.15, str(air_min), ha='center', va='bottom', fontsize=10.5)  # 标出最低空气质量
    plt.xticks(x)
    plt.title('一天空气质量变化曲线图')
    plt.xlabel('时间/h')
    plt.ylabel('空气质量指数AQI')
    plt.show()


def wind_radar(data):
    wind = list(data['风力方向'])
    wind_speed = list(data['风级'])
    for i in range(0, 24):
        if wind[i] == "北风":
            wind[i] = 90
        elif wind[i] == "南风":
            wind[i] = 270
        elif wind[i] == "西风":
            wind[i] = 180
        elif wind[i] == "东风":
            wind[i] = 360
        elif wind[i] == "东北风":
            wind[i] = 45
        elif wind[i] == "西北风":
            wind[i] = 135
        elif wind[i] == "西南风":
            wind[i] = 225
        elif wind[i] == "东南风":
            wind[i] = 315
    degs = np.arange(45, 361, 45)
    temp = []
    for deg in degs:
        speed = []
        # 获取 wind_deg 在指定范围的风速平均值数据
        for i in range(0, 24):
            if wind[i] == deg:
                speed.append(wind_speed[i])
        if len(speed) == 0:
            temp.append(0)
        else:
            temp.append(sum(speed) / len(speed))
    print(temp)
    N = 8
    theta = np.arange(0. + np.pi / 8, 2 * np.pi + np.pi / 8, 2 * np.pi / 8)
    # 数据极径
    radii = np.array(temp)
    # 绘制极区图坐标系
    plt.axes(polar=True)
    # 定义每个扇区的RGB值（R,G,B），x越大，对应的颜色越接近蓝色
    colors = [(1 - x / max(temp), 1 - x / max(temp), 0.6) for x in radii]
    plt.bar(theta, radii, width=(2 * np.pi / N), bottom=0.0, color=colors)
    plt.title('一天风级图', x=0.2, fontsize=20)
    plt.show()


def calc_corr(a, b):
    """计算相关系数"""
    a_avg = sum(a) / len(a)
    b_avg = sum(b) / len(b)
    cov_ab = sum([(x - a_avg) * (y - b_avg) for x, y in zip(a, b)])
    sq = math.sqrt(sum([(x - a_avg) ** 2 for x in a]) * sum([(x - b_avg) ** 2 for x in b]))
    corr_factor = cov_ab / sq
    return corr_factor


def corr_tem_hum(data):
    """温湿度相关性分析"""
    tem = data['温度']
    hum = data['相对湿度']
    plt.scatter(tem, hum, color='blue')
    plt.title("温湿度相关性分析图")
    plt.xlabel("温度/℃")
    plt.ylabel("相对湿度/%")
    plt.text(20, 40, "相关系数为：" + str(calc_corr(tem, hum)), fontdict={'size': '10', 'color': 'red'})
    plt.show()
    print("相关系数为：" + str(calc_corr(tem, hum)))


def tem_curve14(data):
    date = list(data['日期'])
    tem_low = list(data['最低气温'])
    tem_high = list(data['最高气温'])
    for i in range(0, 14):
        if math.isnan(tem_low[i]) == True:
            tem_low[i] = tem_low[i - 1]
        if math.isnan(tem_high[i]) == True:
            tem_high[i] = tem_high[i - 1]

    tem_high_ave = sum(tem_high) / 14
    tem_low_ave = sum(tem_low) / 14

    tem_max = max(tem_high)
    tem_max_date = tem_high.index(tem_max)
    tem_min = min(tem_low)
    tem_min_date = tem_low.index(tem_min)

    x = range(1, 15)
    plt.figure(1)
    plt.plot(x, tem_high, color='red', label='高温')
    plt.scatter(x, tem_high, color='red')
    plt.plot(x, tem_low, color='blue', label='低温')
    plt.scatter(x, tem_low, color='blue')

    plt.plot([1, 15], [tem_high_ave, tem_high_ave], c='black', linestyle='--')
    plt.plot([1, 15], [tem_low_ave, tem_low_ave], c='black', linestyle='--')
    plt.legend()
    plt.text(tem_max_date + 0.15, tem_max + 0.15, str(tem_max), ha='center', va='bottom', fontsize=10.5)
    plt.text(tem_min_date + 0.15, tem_min + 0.15, str(tem_min), ha='center', va='bottom', fontsize=10.5)
    plt.xticks(x)
    plt.title('未来14天温度变化曲线图')
    plt.xlabel('未来天数/天')
    plt.ylabel('摄氏度/℃')
    plt.show()


def change_wind_direction14(wind):
    for i in range(0, 14):
        if wind[i] == "北风":
            wind[i] = 90
        elif wind[i] == "南风":
            wind[i] = 270
        elif wind[i] == "西风":
            wind[i] = 180
        elif wind[i] == "东风":
            wind[i] = 360
        elif wind[i] == "东北风":
            wind[i] = 45
        elif wind[i] == "西北风":
            wind[i] = 135
        elif wind[i] == "西南风":
            wind[i] = 225
        elif wind[i] == "东南风":
            wind[i] = 315
    return wind


def wind_direction_radar14(data):
    wind1 = list(data['风向1'])
    wind2 = list(data['风向2'])
    wind_speed = list(data['风级'])
    wind1 = change_wind_direction14(wind1)
    wind2 = change_wind_direction14(wind2)

    degrees = np.arange(45, 361, 45)
    temp = []
    for degree in degrees:
        speed = []
        # 获取 wind_deg 在指定范围的风速平均值数据
        for i in range(0, 14):
            if wind1[i] == degree:
                speed.append(wind_speed[i])
            if wind2[i] == degree:
                speed.append(wind_speed[i])
        if len(speed) == 0:
            temp.append(0)
        else:
            temp.append(sum(speed) / len(speed))
    print(temp)
    N = 8
    theta = np.arange(0. + np.pi / 8, 2 * np.pi + np.pi / 8, 2 * np.pi / 8)
    # 数据极径
    radii = np.array(temp)
    # 绘制极区图坐标系
    plt.axes(polar=True)
    # 定义每个扇区的RGB值（R,G,B），x越大，对应的颜色越接近蓝色
    colors = [(1 - x / max(temp), 1 - x / max(temp), 0.6) for x in radii]
    plt.bar(theta, radii, width=(2 * np.pi / N), bottom=0.0, color=colors)
    plt.title('未来14天风级图', x=0.2, fontsize=20)
    plt.show()


def weather_pie14(data):
    weather = list(data['气温'])
    dic_wea = { }
    for i in range(0, 14):
        if weather[i] in dic_wea.keys():
            dic_wea[weather[i]] += 1
        else:
            dic_wea[weather[i]] = 1
    print(dic_wea)
    explode = [0.01] * len(dic_wea.keys())
    color = ['yellow', 'salmon', '#cd89fe', 'grey', 'silver', '#3b7afd', '#2ce1e2', '#00ef00', 'pink']
    plt.pie(dic_wea.values(), explode=explode, labels=dic_wea.keys(), autopct='%1.1f%%', colors=color)
    plt.title('未来14天气候分布饼图')
    plt.show()


def main1():
    print("查询天气")
    url1 = 'http://www.weather.com.cn/weather/101100101.shtml'
    url2 = 'http://www.weather.com.cn/weather15d/101100101.shtml'

    html1 = get_html(url1)
    data1, data1_7 = get_content(html1)

    html2 = get_html(url2)
    data8_14 = get_content2(html2)

    data14 = data1 + data8_14
    write_to_csv('weather14.csv', data14,14)
    write_to_csv('weather1.csv', data1_7,1)

def main2():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    data1 = pd.read_csv('weather1.csv', encoding='gbk')
    print(data1)
    tem_curve(data1)
    hum_curve(data1)
    air_curve(data1)
    wind_radar(data1)
    corr_tem_hum(data1)

    data14 = pd.read_csv('weather14.csv', encoding='gb2312')
    print(data14)
    tem_curve14(data14)
    wind_direction_radar14(data14)
    weather_pie14(data14)

if __name__ == '__main__':
    main1()
    main2()