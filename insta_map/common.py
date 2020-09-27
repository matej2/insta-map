import json
import os
from json import JSONEncoder
from random import choice
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "proxies.json")
ua = UserAgent()

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def get_proxies():
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    table = soup.find(id='proxylisttable')
    proxies = list(
        map(lambda x: x[0] + ':' + x[1],
            list(zip(
                map(lambda x: x.text, table.findAll('td')[::8]),
                map(lambda x: x.text, table.findAll('td')[1::8])
                )
            )
        )
    )

    return proxies


def save_proxies():
    proxies = get_proxies()

    with open(dir_path, "w") as file:
        file.write(json.dumps(proxies))
    return True


def get_proxy_from_file():
    with open(dir_path, "r") as file:
        return 'https:' + choice(json.loads(file.read()))


def get_proxy():
    return 'https:' + choice(get_proxies())