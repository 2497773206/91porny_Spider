# -*- coding:utf-8 -*-
import os, time, re, random, requests, urllib3, datetime
from bs4 import BeautifulSoup

URL = 'https://0ksy5j.jiuse710.com'#免翻地址更改位置
cookie = ''
localPath = ''
today = datetime.date.today()

class WebDriver:
    def __init__(self, is_proxy):
        self.session = requests.session()
        self.isProxy = is_proxy
        self.head = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'sec-ch-ua-platform':'"Windows"',
            'sec-fetch-dest':'document',
            'cookie':cookie
        }
        requests.packages.urllib3.disable_warnings()
    def get(self, url):
        return self.session.get(url, timeout=15, headers=self.head, verify=False)
    

def get_user_scr(url):
    userPath = localPath + str(today)
    if os.path.exists(userPath):
        pass
    else:
        os.mkdir(userPath)
    web = WebDriver(False)
    resp = web.get(url)
    bs = BeautifulSoup(resp.text, 'lxml')
    colVideoList = bs.find_all(attrs={'class':'text-truncate title text-sub-title mt-2'})
    for list in colVideoList:
        title = list.text.replace(':','').replace('(','[').replace(')',']').replace('（','[').replace('）',']').replace('“','[').replace('”',']').replace('/','').replace('"','').replace(' ','')
        view_url = URL + list.attrs['href']
        videoName = userPath + '/' + title + '.mp4'
        if os.path.exists(videoName):
            print('目录下已存在相同文件:' + userName + '/' +  title)
            pass
        else:
            time.sleep(random.randint(1, 3))
            view = web.get(view_url)
            view_bs = BeautifulSoup(view.text, 'lxml')
            if view_bs.title.string == '视频因版权原因已被删除':
                print('视频因版权原因已被删除')
                pass
            else:
                view_video = view_bs.select_one("#videoShowPage video")
                data_src = view_video.attrs["data-src"]
                path = os.getcwd() + '/Settings/./ffmpeg -y -i ' + data_src.replace('&','\'&\'') + ' -vcodec copy -acodec copy -absf aac_adtstoasc ' + videoName
                download_m3u8(path)
                #print(userPath)
                with open(os.getcwd() + "/download_info.txt","a",encoding='utf-8') as f:
                    f.write(userPath + '/' + title + '.mp4' + '\n')

def download_m3u8(path):
    os.system(path)

def get_url(url):
    for page in range(1, 4):
        url_page = url + str(page)
        print('当前正在爬取：' + url_page)
        time.sleep(random.randint(1, 3))
        get_user_scr(url_page)

if __name__ == '__main__':
    url = URL + '/video/category/hot-list/'
    get_url(url)
