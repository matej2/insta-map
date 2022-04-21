import os
import random
import time
from random import choice

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "proxies.json")
PROXY_ENABLED = os.environ.get('PROXY_ENABLED') if os.environ.get('PROXY_ENABLED') else False

def get_random_headers():
    ua = UserAgent()
    agent = None

    while agent is None:
        try:
            agent = ua.random
        except:
            print('Failed to get user agent, retrying...')

    return {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'sl',
    }


# Updated script from: https://zenscrape.com/how-to-build-a-simple-proxy-rotator-in-python/
def proxy_generator():
    response = requests.get("https://sslproxies.org/")
    soup = BeautifulSoup(response.content, features='html.parser')

    return {'https': 'http://' + choice(list(map(lambda x: x[0] + ':' + x[1], list(
        zip(map(lambda x: x.text, soup.select('#list td')[::8]),
            map(lambda x: x.text, soup.select('#list td')[1::8]))))))}


def requests_retry_session(
        retries=5,
        backoff_factor=0,
        status_forcelist=0,
        session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


headers = get_random_headers()
proxy = proxy_generator()
c = 10


def get_json(url, proxy=None, c=3):
    response = Response()

    while c > 0:
        try:
            c = c - 1
            if proxy is None:
                proxy = proxy_generator()

            header = get_random_headers()

            time.sleep((random.random() * 2000 + 1000) / 1000)
            if PROXY_ENABLED is True:
                print('Using proxy {}, c={} to reach {}'.format(proxy, c, url))
                response = requests.get(url, timeout=10, proxies=proxy, headers=header)
            else:
                response = requests.get(url, timeout=10, headers=header)

            if response.status_code == 200:
                print('Pass in {}-nth try'.format(c))
                break
            else:
                print('Invalid response code: {}'.format(response.status_code))
        except:
            print('Failed, invalidating proxy')
            proxy = None

    if response.status_code is not None and response.status_code != 200:
        try:
            response = requests.get(url, timeout=10, proxies=proxy, headers=header)
            if response.status_code == 200:
                return response
        except:
            print('Failed withouth proxy')

    try:
        response_json = response.json()
        return response_json
    except:
        print('Failed to decode json')
        return False
