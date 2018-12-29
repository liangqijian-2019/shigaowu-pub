# coding=utf8
import os
import re
import threading
import urllib.request

COOKIE = 'anonymid=jq7o0wjf-yoc40q; depovince=ZGQT; _r01_=1; ick_login=7bbc73b2-7138-4d72-b635-8a8962478915; first_login_flag=1; ln_uact=**************.com; ln_hurl=http://hdn.xnimg.cn/photos/hdn521/20121028/1150/h_main_N8xu_096100008de71375.jpg; loginfrom=syshome; ch_id=10016; JSESSIONID=abcnb3OrbxvAMgoBoIZFw; jebe_key=085b9297-b2c9-4f8b-8b05-516f4d1dfbf2%7C1cbb1033eac0de7357478db49946ee23%7C1545979096709%7C1%7C1545979097006; wp_fold=0; jebecookies=c61792eb-a3e5-41a6-abdc-2cc48385981a|||||; _de=0B725AB25083833A855777BB458B199B6DEBB8C2103DE356; p=7b230a7a254bfabc86d814d8f105b6ce3; t=61e38d9685b8d1e63af60fd61c38e6bd3; societyguester=61e38d9685b8d1e63af60fd61c38e6bd3; id=384806863; xnsid=c7369a3'
HEADERS = {'cookie': COOKIE}
Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
SGW = {'User-Agent':Agent}

# find title
def find_title(mypage):
    myMatch = re.search(r'<title>(.+?)</title>', mypage, re.S)
    title = u'undefined'
    if myMatch:
        title = myMatch.group(1)
    else:
        print(u'find no title')
        # 文件名不能包含以下字符： \ / ： * ? " < > |
        title = title.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"',
                                                                                                                    '').replace(
            '>', '').replace('<', '').replace('|', '')
    return title


def login_renren(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        req.add_header("User-Agent",Agent)
        page = urllib.request.urlopen(req).read()
        page = page.decode('utf-8')
        title = find_title(page)
        print(title)
        return page
    except:
        page = r''
        return page


def find_friendlist():
    url_friend = 'http://friend.renren.com/groupsdata'  # friend list
    req = urllib.request.Request(url_friend, headers=HEADERS)
    try:
        page = urllib.request.urlopen(req).read()
        page = page.decode('utf-8')
    except:
        print('cookie is error')
        page = ''
    pattern = re.compile(r'"fid":\d*?,')
    if pattern.findall(page):
        list = pattern.findall(page)
        friend_file = open('id.txt', 'w')
        for i in list:
            id = i[6:-1]
            friend_file.write(id)
            friend_file.write(os.linesep)
        friend_file.close()
    else:
        print('find no friendID')


# http://photo.renren.com/photo/XXXXXXXXX/album/relatives/profile
# http://photo.renren.com/photo/XXXXXXXXX/album-535947620?frommyphoto
def find_ablumUrl():
    list = r''
    file = open('id1.txt')
    ablum = open('albumlist.txt', 'w')
    while 1:
        line = file.readline()
        if line:
            line = line[:-1]
            photo_url = 'http://photo.renren.com/photo/348359757/album-538490587/v7'
            print(photo_url)
            data = login_renren(photo_url)
            pattern = re.compile(r'http://photo.renren.com/photo/')
            if pattern.findall(data):
                list = pattern.findall(data)
            else:
                print('find no album id')
                # remove duplicate album id
            albumid_set = set()
            for i in list:
                albumid_set.add(i)

            for i in albumid_set:
                album_list = 'http://photo.renren.com/photo/348359757/album-538490587/v7'
                print(album_list)
                ablum.write(album_list)
                ablum.write(os.linesep)
        else:
            break


def download_album():
    file = open('albumlist.txt')
    while 1:
        line = file.readline()
        if not line:
            break
        else:
            list = ''
            data = login_renren(line)
            pattern = re.compile(r'http://fmn.rrimg.com/.*?/.*?/.*?/original_.*?_.*?\.jpg', re.I)  # large xlarge
            if pattern.findall(data):
                list = pattern.findall(data)
            else:
                print('found no image')

            photo_url = set()
            for i in list:
                i = i[:]
                photo_url.add(i)
                print(i)  # test
            try:
                d = Download(photo_url)
                print(d.name)
                d.start()
            except:
                print(u'download error   ' + line)
    file.close()


# download by thread
class Download(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.que = que

    def run(self):
        for i in self.que:
            req = urllib.request.Request(i, headers=SGW)
            data = urllib.request.urlopen(req).read()
            path = str(i[-16:-5]) + '.jpg'
            f = open(path, 'ab')  # 存储下载的图片
            f.write(data)
            f.close()
        return


# start
def start_photo_grap():
    login_renren(URL)
    find_friendlist()
    find_ablumUrl()
    download_album()


URL = r'http://www.renren.com'

if __name__ == '__main__':
    start_photo_grap()

