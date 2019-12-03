import requests
from bs4 import BeautifulSoup
import re
import json
import urllib.request
import os
from tqdm import tqdm
import sys

class KakaoEmoticon:
    def __init__(self, url):
        headers = {
            'User-Agent': "Mozilla/5.0(Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36(KHTML, "
                          "like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36(compatible; Googlebot/2.1; "
                          "+http://www.google.com/bot.html)",
        }
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        title = soup.find('meta', attrs={'property': "og:title"}).get('content')
        sample = soup.find('meta', attrs={'property': "og:image"}).get('content')
        item_code = int(
            str(soup).split('item_code')[1].split('}')[0].replace(' ', '').replace('\n', '').replace('\'', '').replace(
                ':', ''))
        res = requests.get("https://e.kakao.com/detail/thumb_url?item_code=" + str(item_code))
        res = res.json()
        self.item_code = item_code
        self.imageURL = res['body']
        self.title = title
        self.sample = sample

    def download(self):
        temp = 1
        output = os.getcwd() + "\\" + self.title + "\\"
        if not os.path.isdir(output):
            os.makedirs(output)

        for i in tqdm(self.imageURL):
            urllib.request.urlretrieve(i, output + str(temp) + '.png')
            temp = temp + 1

def main(string):
    KakaoEmoticon(string).download()

if __name__ == "__main__":
    main(sys.argv[1])


