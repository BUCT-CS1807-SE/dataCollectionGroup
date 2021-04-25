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
        brief_introduction = tree.xpath('//div[@class="cont c666 font16"]/text()')
        print(url)
        print(brief_introduction)
        sheet.cell(row=i+1,column=1).value=brief_introduction[0]
    wb.save('补充信息.xlsx')
visit_site_basic_information()
