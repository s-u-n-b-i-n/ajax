#-*-coding:utf-8-*
# python2默认以ASCII编码，但是在实际编码过程中，我们会用到很多中文
from urllib import urlencode
#urlencode 可以将字典转化为字符串
import requests
from pyquery import PyQuery as pq  #引入PyQuery 对象

base_url = "https://m.weibo.cn/api/container/getIndex?"
headers = {
    'Referer': 'https://m.weibo.cn/u/2830678474', #访问来源
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
# type=uid&value=2830678474&containerid=1076032830678474&page=3
def get_page(page):
    params = {
        'type':'uid',
        'value':'2830678474',
        'containerid':'1076032830678474',
        'page':page
    }
    # get请求：url+params
    # urlencode 将字典转化为字符串的形式，便于get方法提交的时候进行传参
    url = base_url + urlencode(params)
    try:
        response = requests.get(url = url ,headers =headers)
        if(response.status_code == 200):
            return response.json()
        else :
            print(response.status_code)
    except requests.ConnectionError as e:
        print('Error',e.args)

import json
def parse_page(json1):
    if json1:
        items= json1['data']['cards']  #根据key取value
        # print(type(items))  #<type 'list'>
        # print(items)
        weibo = {}
        for item in items:
            if  'mblog' in item:
                item = item['mblog']
                # print(type(item))  # <type 'dict'>
                weibo['id'] = item['id']
                item_str = item['text']
                # print(type(item_str))  #<type 'unicode'>
                doc = pq(item_str)  #将字符串当做参数传给PyQuery类，完成初始化
                # print(doc)
                weibo['text'] = doc.text() #微博正文
                # print(doc.text())
                weibo['attitudes'] =  item['attitudes_count'] #点赞个数
                weibo['reposts'] = item['reposts_count']   #转发个数
                # print(json.dumps(weibo, encoding='utf-8', ensure_ascii=False))
            else:
                print(json.dumps(item,encoding='utf-8',ensure_ascii=False))
                # print("不含mblog:",item)
            # yield weibo
            yield(json.dumps(weibo,encoding='utf-8',ensure_ascii=False))
    else:
        print("1234")

from pymongo import MongoClient

client = MongoClient()
db = client['weibo']
collection = db['weibo']

# 将数据保存在mongoDB中
def save_to_mongo(result):
    result_final = json.loads(result)
    # print(type(result_final))
    if collection.insert(result_final):
        print('save to mongo!!!')

if __name__ == '__main__':
    for page in range(1,11):
    #     page = 1
        get_json = get_page(page)  # response
        # print(type(json)) # <type 'dict'>
        results = parse_page(get_json)
        for result in results:
            print(result)
            save_to_mongo(result)




