'''
解决md文档显示图片的问题:
    下载md文件中的图片 保存至文件夹中 以相对路径的形式在md文档中展示
'''
import re
import os
import requests

mytxt = ''
urlInfo = []


def readfile(filename):
    global mytxt
    with open(filename, 'r', encoding='utf-8') as f:
        mytxt = f.read()


def downImageTosave():
    global urlInfo
    urlInfo = re.compile('(https://note.youdao.com.*)\)').findall(mytxt)
    headers = {
        'user-agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Cookie':
        'OUTFOX_SEARCH_USER_ID=-1041197138@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=1285372515.232096; Hm_lvt_daa6306fe91b10d0ed6b39c4b0a407cd=1632421149; _ga=GA1.2.593420780.1632421151; YNOTE_SESS=v2|RxpANvOraBlGOMP4PM6F0YEhHgukL6K0TykL6unfwz0wuRfPunMqL0Qz6MqzO464RPFkfYG64YWRJFRLeuh4JK0qFkMeLhfzA0; YNOTE_LOGIN=1||1632709980583; YNOTE_CSTK=2k5XDyuB; Hm_lpvt_daa6306fe91b10d0ed6b39c4b0a407cd=1632837921; DICT_UGC=be3af0da19b5c5e6aa4e17bd8d90b28a|; JSESSIONID=abch5A0VJd0Nv52xTWWWx; _ntes_nnid=ef15a1e2011b6d65b6716b5d6fbe4a27,1632905652084123456'
    }
    dir_name = 'Screenshots'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        for index, img_url in enumerate(urlInfo):
            reponse = requests.get(img_url, headers=headers)
            if reponse.status_code == 200:
                with open(dir_name + '/' + str(index) + '.jpg', 'wb') as f:
                    f.write(reponse.content)


def repToMD():
    global mytxt
    for index, img_url in enumerate(urlInfo):
        rep = 'Screenshots/' + str(index) + '.jpg'
        # 注意: replace不会改变原字符串！
        mytxt = mytxt.replace(img_url, rep)

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(mytxt)


def main():
    readfile('readme.txt')
    downImageTosave()
    repToMD()
    # 验证
    # print(re.compile('(Screenshots/.*)\)').findall(mytxt))


main()
