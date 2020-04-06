import requests
from bs4 import BeautifulSoup
import urllib.request
import os
from tqdm import tqdm
import sys
import platform

class KakaoEmoticonJSON:
    def __init__(self, itemcode):
        self.itemcode = itemcode
        self.imageURL = requests.get("https://e.kakao.com/detail/thumb_url?item_code=" + str(itemcode)).json()['body']
    def download(self):
        print("Downloading from Kakao Emoticon Database"+ "\n")
        if platform.system() == 'Windows':
            temp = 1
            output = os.getcwd() + "\\" + str(self.itemcode) + "\\"
            if not os.path.isdir(output):
                os.makedirs(output)

            for i in tqdm(self.imageURL):
                urllib.request.urlretrieve(i, output + str(temp) + '.png')
                temp = temp + 1
        else:
            temp = 1
            output = os.getcwd() + "/" + str(self.itemcode) + "/"
            if not os.path.isdir(output):
                os.makedirs(output)

            for i in tqdm(self.imageURL):
                urllib.request.urlretrieve(i, output + str(temp) + '.png')
                temp = temp + 1

class KakaoEmoticon:
    def __init__(self, url):
        url = url.replace(' ', '-')
        if url.find("http://") != 0 and url.find("https://") != 0:
            if url.find("http://e.kakao.com/t/") != 0 and url.find("https://e.kakao.com/t/") != 0:
                url = "https://e.kakao.com/t/" + url
            else:
                print("Input protocol is set as https because input protocol is omitted.")
                url = "https://" + url
        headers = {
            'User-Agent': "Mozilla/5.0(Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36(KHTML, "
                          "like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36(compatible; Googlebot/2.1; "
                          "+http://www.google.com/bot.html)",
        }
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        item_code = int(
            str(soup)
                .split('item_code')[1]
                .split('}')[0]
                .replace(' ', '')
                .replace('\n', '')
                .replace('\'', '')
                .replace(':', '')
        )
        res = requests.get("https://e.kakao.com/detail/thumb_url?item_code=" + str(item_code))
        res = res.json()
        self.url = url
        self.item_code = item_code
        self.imageURL = res['body']
        self.title = soup.find('meta', attrs={'property': "og:title"}).get('content')
        self.sample = soup.find('meta', attrs={'property': "og:image"}).get('content')

    def download(self):
        print("Downloading from " + self.url + "\n")
        if platform.system() == 'Windows':
            temp = 1
            output = os.getcwd() + "\\" + self.title + "\\"
            if not os.path.isdir(output):
                os.makedirs(output)

            for i in tqdm(self.imageURL):
                urllib.request.urlretrieve(i, output + str(temp) + '.png')
                temp = temp + 1
        else:
            temp = 1
            output = os.getcwd() + "/" + self.title + "/"
            if not os.path.isdir(output):
                os.makedirs(output)

            for i in tqdm(self.imageURL):
                urllib.request.urlretrieve(i, output + str(temp) + '.png')
                temp = temp + 1

def force_download(string):
    KakaoEmoticonJSON(string).download()

def download(string):
    KakaoEmoticon(string).download()

def title(string):
    print(KakaoEmoticon(string).title)

def sample(string):
    print(KakaoEmoticon(string).sample)

help = """
Command:
    -h or --help     : Display commands list.
    -d or --download : Download Kakao Emoticons.
    -t or --title    : Display emoticon's title.
    -s or --sample   : Display sample image link.
    -i or --itemcode : Download Kakao Emoticon with itemcode.
    
Example:
    KakaoEmoticonDownloader -d the-girl-in-pajamas-ver-2
    KakaoEmoticonDownloader -d "the girl in pajamas ver 2"
    KakaoEmoticonDownloader -d e.kakao.com/t/the-girl-in-pajamas-ver-2
    KakaoEmoticonDownloader -d http://e.kakao.com/t/the-girl-in-pajamas-ver-2
    KakaoEmoticonDownloader -d https://e.kakao.com/t/the-girl-in-pajamas-ver-2
    KakaoEmoticonDownloader -i 2220381"""

prog = """
Kakao Emoticon Downloader
This program is for using paid kakao emoticon in other messenger
so if you didn't pay their emoticons, don't use this program.
This program cannot be used for commercial purposes."""

if __name__ == "__main__":
    if len(sys.argv) != 1:
        if (sys.argv[1] == '-d' or sys.argv[1] == "--download"):
            download(sys.argv[2])
        elif (sys.argv[1] == '-i' or sys.argv[1] == "--itemcode"):
            force_download(sys.argv[2])
        elif (sys.argv[1] == '-h' or sys.argv[1] == "--help"):
            print(help)
        elif (sys.argv[1] == '-s' or sys.argv[1] == "--sample"):
            sample(sys.argv[2])
        elif (sys.argv[1] == '-t' or sys.argv[1] == "--title"):
            title(sys.argv[2])
        else:
            print("Command Not found : " + sys.argv[2])
    else:
        print(prog+"\n"+help)
