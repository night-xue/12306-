import requests
import pandas as pd
import json
from tqdm import tqdm
import RobTickets

pd.set_option('display.max_columns', 2000)
pd.set_option('display.max_rows', 2000)
pd.set_option('display.width', 2000)
pd.set_option('display.unicode.ambiguous_as_wide',True)
pd.set_option('display.unicode.east_asian_width',True)

f = open('city.json', encoding='utf-8')
# print(f.read())
txt = f.read()
json_data = json.loads(txt)
from_station = input('请输入出发城市： ')
to_station = input('请输入到达城市： ')
date = input('请输入你要出发的日期（格式：2022-01-01）：')

url = f'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={json_data[from_station]}&leftTicketDTO.to_station={json_data[to_station]}&purpose_codes=ADULT'

headers = {
    # 用户信息，常用于检测是否登陆账号
    'Cookie': 'tk=k8aL58-FmMijK_M7iOqWe7b6RxsoDC-mhP7O4Qtyx1x0; JSESSIONID=F1C94FB5A60AB777D088BE51E8FD7E58; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; RAIL_EXPIRATION=1668598513048; RAIL_DEVICEID=Jo2I1xeK2U7JvDJvKISuVvg-hC9Bdr07qqQ2n497ouEt9ElLi5iCI3QWvND0l17aNIxOfyAMXeyLyxFmqvzJGa8mqZLt3DmVeQtCAgATQ2JSl_Lw3cPs2sLb3jrM6_poLy402k0-PZvZoAUL3CT4WK6iCmW1312L; _jc_save_fromStation=%u592A%u539F%u5357%2CTNV; _jc_save_toStation=%u4FAF%u9A6C%u897F%2CHPV; _jc_save_fromDate=2022-11-21; _jc_save_toDate=2022-11-21; _jc_save_wfdc_flag=wf; BIGipServerotn=351273482.38945.0000; BIGipServerpool_passport=266600970.50215.0000; route=495c805987d0f5c8c84b14f60212447d; fo=my2oya6i0t302mpsilOJbG3nsdQ7uynLlKl5ZNr8ExDsUCHDQzOFLKLPLbmVfuNLvf0KjQuUWjdci96EKdYC8Gcz0glggrG1wQXp9dINeVzBhlXQ2B4hrXOdlvCslKUVofj7QILo1UL0Y2CY0HG-Bqx1PulKV0SPWupouZwQxEkEqVuLCfPGsanhWpo; current_captcha_type=Z',
    # User-Agent:用户代理，浏览器基本身份标识
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42',
    'Host': 'kyfw.12306.cn',
    'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init'
}
# 通过requests数据请求模块里的get请求方法，对于url地址发送请求，携带上headers请求头伪装，最后用response变量接收返回数据
response = requests.get(url=url,headers=headers)
response.encoding = response.apparent_encoding
# print(response)
print(response.json())
# print(response.text)

result = response.json()['data']['result']
lis = []
for index in tqdm(result):
#      index.split('|')
#      print(index)
#      page = 0
#      for i in index.split('|'):
#          print(i,page,sep='|')
#          page += 1
#      break
# #
    info = index.replace('有','Y').replace('无','N').split('|')
    num = info[3]
    start_time = info[8]
    end_time = info[9]
    use_time = info[10]
    topGrade = info[32]
    first_class = info[31]
    second_class = info[30]
    soft_sleeper = info[23]
    hard_sleeper = info[28]
    hard_seat = info[29]
    no_seat = info[26]
    dit = {
        'num': num,
        'start_time': start_time,
        'end_time': end_time,
        'use_time': use_time,
        'topGrade': topGrade,
        'first_class': first_class,
        'second_class': second_class,
        'soft_sleeper': soft_sleeper,
        'hard_sleeper': hard_sleeper,
        'hard_seat': hard_seat,
        'no_seat': no_seat
    }
    lis.append(dit)
    print(lis)
# #
# #
columns = ['num','start_time','end_time','use_time','topGrade','first_class','second_class','soft_sleeper','hard_sleeper','hard_seat','no_seat']
content = pd.DataFrame(lis,columns=columns)
print(content)
content.to_csv('data.csv',encoding='gbk')
RobTickets.get_ticket(from_station,to_station,date)


