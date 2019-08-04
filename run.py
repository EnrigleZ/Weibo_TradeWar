#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import time 
import random
import json


# In[2]:


base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%E8%B4%B8%E6%98%93%E6%88%98',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15',
    'X-Requested-With': 'XMLHttpRequest',
    'MWeibo-Pwa': '1'
}


# In[72]:


def query_page(query, page=''):
    params = {
        'containerid': '100103type=1&q=%s'%query,
        'page_type': 'searchall',
        'page': page
    }
    url = base_url + urlencode(params)
    print(url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(e)


# In[37]:


def save_json(result, title):
    path = './data/%s.json'%title
    with open(path, 'ab') as f:
        f.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
        f.write('\r\n'.encode('utf-8'))


# In[74]:


def process_item(item):
    ret = {}
    assert item.get('card_type') == 9
    mblog = item.get('mblog')
    id = mblog.get('id') # ?mid
    created_at = mblog.get('created_at')
    text = mblog.get('text')
    if 'longText' in mblog:
        text = mblog.get('longText').get('longTextContent')
    user = mblog.get('user')
    ret['id'] = id
    ret['created_at'] = created_at
    ret['text'] = text
    ret['user'] = user
    return ret


# In[78]:


def collect_weibo(query, max_page=10, save=False):
    ret = []
    all_items.clear()
    invalid_items.clear()
    for page in range(1, max_page+1):
        response_json = query_page(query, page)
        if save: save_json(response_json, '%s-%d'%(query, page))
        if response_json.get('ok') == 1 and response_json.get('data') is not None:
            cards = response_json.get('data').get('cards', {})
            
            for card in cards:
                
                if 'card_group' not in card: continue
                for item in card['card_group']:
#                     all_items.append(item)
                    if item.get('card_type') != 9: continue
                    ret.append(process_item(item))
                    
            time.sleep(1)
    
    print('Fetch %d records'%len(ret))
    return ret


# In[79]:


res = collect_weibo('龟龟', 3, save=True)
print(res[0])


# In[50]:


all_items = []
invalid_items = []


# In[16]:


test = {
    'arg1': '',
    'arg2': None
}
test.get('asd', 0)


# In[61]:


# save_json(all_items, 'all')
valids = list(filter(lambda x: 'mblog' in  x, all_items))

