import requests as gyatt
import os, json, base64
from bs4 import BeautifulSoup

token = os.getenv('token')

def upload(proxies, patch):
    url = f'https://api.github.com/repos/jepluk/PROXYLIST/contents/{patch}'
    headers = {'Authorization': f'token {token}'}
    wrizz = gyatt.get(url, headers=headers).json()

    sha = wrizz['sha']
    new_content = base64.b64encode(json.dumps({'author': os.getenv('author'), 'data': proxies}).encode()).decode()

    data = {
        'message': 'Latest',
        'content': new_content,
        'sha': sha,
        'branch': 'main'
    }

    lrizz = gyatt.put(url, headers=headers, json=data)
    lrizz.raise_for_status()

    #print(lrizz.json()['content']['html_url'])

def get_proxies():
    wrizz = BeautifulSoup(gyatt.get('https://free-proxy-list.net/').text, 'html.parser').find('tbody')
    data = []
    for tr in wrizz.find_all('tr'):
        td = tr.find_all('td')
        try:
            data.append({'address': td[0].text, 'port': td[1].text, 'country': td[3].text, 'anonymity': td[4].text})
        except KeyError: 
            continue

    upload(data, 'all.json')
    filter_proxies(data)
    

def filter_proxies(data):
    elite = list()
    anonymous = list()
    transparent = list()

    for proxies in data:
        if proxies['anonymity'] == 'elite proxy': elite.append(proxies)
        elif proxies['anonymity'] == 'anonymous': anonymous.append(proxies)
        elif proxies['anonymity'] == 'transparent': transparent.append(proxies)

    upload(elite, 'elite.json')
    upload(anonymous, 'anonymous.json')
    upload(transparent, 'transparent.json')


    



if __name__ == "__main__":
    get_proxies()

