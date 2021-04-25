import requests
from lxml import etree
import pandas as pd
import openpyxl
from tqdm import tqdm

# 1.指定url
all_data = list(pd.read_csv('博物馆信息.csv')['博物馆对应页面的编号'])  # 拿到所有页面的编号


def visit_site_basic_information():  # 开始按照网址访问网站，并填写基本信息
    # 2.UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    fixed_title = list(pd.read_excel('补充信息.xlsx'))
    wb = openpyxl.load_workbook('补充信息.xlsx')
    for i in tqdm(range(len(all_data))):
        sheet = wb.active
        url = 'https://www.maigoo.com/citiao/' + str(all_data[i]) + '.html'  # 指定网址
        # 3.获取源码内容
        # print(url)
        page_text = requests.get(url=url, headers=headers).text
        # 4.生成实例对象
        tree = etree.HTML(page_text)
        # 下面一次性可以将博物馆所处于的地址信息，票价，开馆时间、建议游玩时间、博物馆类型、国际级别、第几批选入的国家一级博物馆、旅游景区的级别
        basic_information_title = tree.xpath('//div[@class="lbox"]/em[@class="fcolor bdcolor"]/text()')
        basic_information = tree.xpath('//div[@class="lbox"]/span[@class="c666 dhidden"]/text()')
        # 因为title的格式不符合csv当中的格式，因此需要进行修改
        if '官网：' in basic_information_title:
            basic_information_title.remove('官网：')
        for j in range(len(basic_information_title)):  # 遍历是为了生成新的标题，并且满足csv中的标题
            temp_title = str(basic_information_title[j])
            temp_title = temp_title[:-1]
            if temp_title in fixed_title:
                index = fixed_title.index(temp_title)
                sheet.cell(row=i + 2, column=index + 1).value = basic_information[j]
# 根据格式化将信息保存下来
        # 需要将其填入到表格当中，需要确保将标题相同的信息填入到表格当中
    wb.save('补充信息.xlsx')
    # print(basic_information_title)


visit_site_basic_information()
