# -*- coding:utf-8 -*-
import os, time, re, random, requests, urllib3
from bs4 import BeautifulSoup

URL = 'https://0ksy5j.jiuse710.com'#免翻地址更改位置


class WebDriver:
    def __init__(self, is_proxy):
        self.session = requests.session()
        self.isProxy = is_proxy
        self.head = {
            'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
        }
        requests.packages.urllib3.disable_warnings()
    def get(self, url):
        return self.session.get(url, timeout=11, headers=self.head, verify=False)
    

def user(url):
    userName = getpage(url)[0]
    userPath = '/data/Videos/91porny/' + userName
    if os.path.exists(userPath):
        pass
    else:
        os.mkdir(userPath)
    web = WebDriver(False)
    resp = web.get(url)
    bs = BeautifulSoup(resp.text, 'lxml')
    colVideoList = bs.find_all(attrs={'class':'text-truncate title text-sub-title mt-2'})
    for list in colVideoList:
        title = list.text
        view_url = 'https://0ksy5j.jiuse710.com' + list.attrs['href']
        view = web.get(view_url)
        view_bs = BeautifulSoup(view.text, 'lxml')
        #print(view_bs.title.string)
        if view_bs.title.string == '视频因版权原因已被删除':
            print('视频因版权原因已被删除')
            pass
        else:
            view_video = view_bs.select_one("#videoShowPage video")
            data_src = view_video.attrs["data-src"]
            videoName = userPath + '/' + title + '.mp4'
            path = os.getcwd() + '/Settings/./ffmpeg -y -i ' + data_src.replace('&','\'&\'') + ' -vcodec copy -acodec copy -absf aac_adtstoasc ' + videoName
            if os.path.exists(videoName):
                print('目录下已存在相同文件')
                pass
            else:
                download_m3u8(path)
                with open(os.getcwd() + "/download_info.txt","a",encoding='utf-8') as f:
                    f.write(userPath + '/' + title + '.mp4' + '\n')

def download_m3u8(path):
    print(path)
    os.system(path)

def user_url():
    path = r"userurl.txt"
    file = open(path,"r",encoding="utf-8",errors="ignore")
    while True:
        mystr = file.readline()#表示一次读取一行
        if not mystr:
            break
        url = mystr
        enter(url)

def enter(url):
    end = int(getpage(url)[1]) + 1
    for page in range(1, end):
        url_page = url + '?page=' + str(page)
        print('当前正在爬取：' + url_page)
        time.sleep(random.randint(1, 3))
        user(url_page)

def getpage(url):
    web1 = WebDriver(False)
    resp1 = web1.get(url)
    bs1 = BeautifulSoup(resp1.text, 'lxml')
    page = bs1.find_all(attrs={'class':'container-title col-60'})
    for list in page:
        page_text = list.text.split('/', 1)
        user_name_result = re.findall("“(.*)”",page_text[0])
        for x in user_name_result:
            user_name = x
        page_page = page_text[1].replace('页','')
        return user_name, page_page

if __name__ == '__main__':
    print('1、文件爬取   2、手动爬取')
    zone = input('请输入爬取模式：')
    if int(zone) == 1:
        file = open("download_info.txt", 'w').close()
        file1 = open("userurl.txt", 'w').close()
        user_url()
        print('爬取完毕')
    elif int(zone) == 2:
        file = open("download_info.txt", 'w').close()
        url = input('请输入需要爬取的链接：')
        enter(url)
        print('爬取完毕')
