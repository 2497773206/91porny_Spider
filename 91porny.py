# -*- coding:utf-8 -*-
import os, time, re, random, requests, urllib3
from bs4 import BeautifulSoup
from faker import Faker

URL = 'https://0ksy5j.jiuse710.com'#免翻地址
cookie = 'PHPSESSID=ee7d416eab164a7a8cf23d24159905c7;'#更新cookie
localPath = '/data2/Videos/91porny/'#保存路径（确保存在该路径）

class WebDriver:
    def __init__(self, is_proxy):
        self.session = requests.session()
        self.isProxy = is_proxy
        self.head = {
            'user-agent':fakeua.chrome(),
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'sec-ch-ua-platform':'"Windows"',
            'sec-fetch-dest':'document',
            'cookie':cookie
        }
        requests.packages.urllib3.disable_warnings()
    def get(self, url):
        time.sleep(0.5)
        return self.session.get(url, timeout=15, headers=self.head, verify=False)
    

def get_user_scr(url):
    userName = get_page_src(url)[0]
    userPath = localPath + userName
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

def get_updata_scr(url):
    userName = get_page_src(url)[0]
    userPath = localPath + userName
    if os.path.exists(userPath):
        pass
    else:
        os.mkdir(userPath)
    web = WebDriver(False)
    resp = web.get(url)
    bs = BeautifulSoup(resp.text, 'lxml')
    colVideoList = bs.find_all(attrs={'class':'text-truncate title text-sub-title mt-2'})
    videoSrc = colVideoList[:15]#需要下载视频的数量
    for list in videoSrc:
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

def user_url():
    path = r"userurl.txt"
    file = open(path,"r",encoding="utf-8",errors="ignore")
    while True:
        mystr = file.readline()#表示一次读取一行
        if not mystr:
            break
        url = mystr
        get_url(url)

def updata_url():
    path = r"updata.txt"#更新链接
    file = open(path,"r",encoding="utf-8",errors="ignore")
    while True:
        mystr = file.readline()#表示一次读取一行
        if not mystr:
            break
        url = mystr
        get_updata_scr(url)

def get_url(url):
    end = int(get_page_src(url)[1]) + 1
    for page in range(1, end):
        url_page = url + '?page=' + str(page)
        print('当前正在爬取：' + url_page)
        time.sleep(random.randint(1, 3))
        get_user_scr(url_page)

def get_page_src(url):
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
    print('1、批量爬取   2、单独爬取   3、更新视频')
    zone = input('请输入爬取模式：')
    if int(zone) == 1:
        file = open("download_info.txt", 'w').close()
        user_url()
        print('爬取完毕')
        file1 = open("userurl.txt", 'w').close()
    elif int(zone) == 2:
        file = open("download_info.txt", 'w').close()
        url = input('请输入需要爬取的链接：')
        get_url(url)
        print('爬取完毕')
    elif int(zone) == 3:
        file = open("download_info.txt", 'w').close()
        updata_url()
        print('爬取完毕')


