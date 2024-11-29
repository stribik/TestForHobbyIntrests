import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 设置代理
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890', 
}

# URL为目标网页地址,这里清手动填一下QAQ
url = ' '

# 创建result文件夹
if not os.path.exists('result'):
    os.makedirs('result')

response = requests.get(url, proxies=proxies)
soup = BeautifulSoup(response.text, 'html.parser')

gallery_items = soup.find_all('li')

items = []

for item in gallery_items:
    img_tag = item.find('img')
    img_url = img_tag['src'] if img_tag else None

    h5_tag = item.find('h5')
    title = h5_tag.get_text(strip=True) if h5_tag else None

    if img_url:
        img_url = urljoin(url, img_url)
    
        img_name = img_url.split('/')[-1]
        img_data = requests.get(img_url, proxies=proxies).content
        with open(os.path.join('result', img_name), 'wb') as f:
            f.write(img_data)
        items.append({'title': title, 'img_name': img_name, 'img_url': img_url})
for item in items:
    print(f"Title: {item['title']}, Image saved as: result/{item['img_name']}")
