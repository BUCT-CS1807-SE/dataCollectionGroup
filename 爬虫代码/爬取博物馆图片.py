import re
import requests
import os
from lxml import etree
import pandas as pd
from tqdm import tqdm


if not os.path.exists('./photos'): # 创建一个/photos文件夹，里面用于存放所有图片
    os.mkdir('./photos')
all_data = list(pd.read_csv('博物馆信息.csv')['博物馆对应页面的编号'])  # 拿到所有页面的编号
names=list(pd.read_csv('博物馆信息.csv')['博物馆名称'])
all_images=[]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0'
}
for i in tqdm(range(len(all_data))):
    url='https://www.maigoo.com/citiao/'+str(all_data[i])+'.html'
    page_text=requests.get(url=url,headers=headers).text
    tree=etree.HTML(page_text)
    image=tree.xpath('//span[@class="showauthor"]/img/@src')
    if len(image)==0:
        image=tree.xpath('//span[@class="showauthor"]/a/img/@src')
    if len(image)==0:
        image=['没有发现图片']
    all_images.append(image[0])
count=0
for image_url in tqdm(all_images):
    if image_url=='没有发现图片':
        count+=1
        continue
    image_path = './photos/'+str(names[count])+'.jpg'
    image_data = requests.get(image_url, headers=headers).content
    with open(image_path, 'wb') as fp:
        fp.write(image_data)
        print(str(names[count])+'下载完成')
    count+=1



