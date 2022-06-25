import re

from bs4 import BeautifulSoup
import requests
import os

def get_type_list(url : str):
    type_list = []
    type_list.append("https://www.imn5.net/XiuRen/XiuRen/")

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
    }

    res = requests.get(url, headers=header)

    res.encoding = "utf-8"

    html = res.text

    soup = BeautifulSoup(html, "lxml")

    liclass = soup.find_all(
        name="liclass"
    )

    second_html = liclass[1]

    a_list = second_html.find_all('a')

    for one in a_list:
        href = one.get('href')
        type_list.append("https://www.imn5.net" + href)
    return type_list

def get_one_type_all_page_url_list(url):
    url_list = []
    url_list.append(url)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
    }
    res = requests.get(url, headers=header)
    res.encoding = "utf-8"
    html = res.text
    soup = BeautifulSoup(html, "lxml")
    page = soup.find_all(
        name="div",
        attrs={
            "class": "page"
        }
    )[0].find_all(
        name="a"
    )

    if (len(page) > 8):
        p = re.findall('\d+', page[-1].get('href'))
        total_page = int(p[0])
    elif (1 < len(page) <= 8):
        total_page = len(page) - 1
    else:
        total_page = 1

    if(total_page == 1):
        return url_list
    else:
        for i in range(1,total_page):
            url_list.append(url+"list"+str(i+1)+".html")
    return url_list

def get_one_page_thumbnail_url_list(url:str):
    url_list = []
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
    }
    res = requests.get(url, headers=header)

    res.encoding = "utf-8"
    html = res.text
    soup = BeautifulSoup(html, "lxml")
    thumbnail_list = soup.find_all(
        name="article",
        attrs={
            "class": "excerpt-c5"
        }
    )
    for ori_html in thumbnail_list:
        detail_url = ori_html.find(
            name="h2"
        ).find(name="a").get("href")
        url_list.append("https://www.imn5.net"+detail_url)

    return url_list

def get_detail_page_url_list(url):
    url_list = []
    res = requests.get(url)
    res.encoding = "utf-8"
    html = res.text
    soup = BeautifulSoup(html, "lxml")
    page = soup.find_all(
        name="div",
        attrs={
            "class": "page"
        }
    )[0].find_all(
        name="a"
    )

    page = page[0:-1]
    for one in page:
        one_picture_url = one.get("href")
        url_list.append("https://www.imn5.net"+one_picture_url)

    dir_name = soup.find(
        name="div",
        attrs={
            "class": "focusbox"
        }
    ).find(
        name="div",
        attrs={
            "class": "container"
        }
    ).find(
        name="div"
    ).get_text()

    return url_list, dir_name

def get_detail_page_img_url_list(url:str):
    url_list = []
    res = requests.get(url)
    res.encoding = "utf-8"
    html = res.text
    soup = BeautifulSoup(html, "lxml")
    img_list = soup.find_all(
        name="div",
        attrs={
            "class": "imgwebp"
        }
    )[0].find_all(
        name="img"
    )
    for one in img_list:
        pic_real_url = one.get("src")[11:]
        url_list.append("https://pic.imn5.net/Uploadfile"+pic_real_url)
    return url_list

def create_dir_not_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print("新文件夹创建成功...")

def download_pic_from_url(url : str, path:str):
    pic = requests.get(url)
    img = pic.content
    pic_name = url[-16:-5]
    with open(path + '/' + pic_name + '.jpg', 'wb') as f:
        f.write(img)
        f.close()
        print(pic_name+"：下载成功...")


if __name__ == '__main__':
    url = "https://www.imn5.net/XiuRen/XiuRen/"
    type_list = get_type_list(url)
    for type in type_list:
        one_type_all_page_url_list = get_one_type_all_page_url_list(type)
        for one_type_all_page_url in one_type_all_page_url_list:
            one_page_thumbnail_url_list = get_one_page_thumbnail_url_list(one_type_all_page_url)
            for one_page_thumbnail_url in one_page_thumbnail_url_list:
                detail_page_url_list, dir_name = get_detail_page_url_list(one_page_thumbnail_url)
                path = 'aimeinv/'+dir_name
                create_dir_not_exist(path)
                for detail_page_url in detail_page_url_list:
                    detail_page_img_url_list = get_detail_page_img_url_list(detail_page_url)
                    for detail_page_img_url in detail_page_img_url_list:
                        download_pic_from_url(detail_page_img_url, path)









