from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

def get_one_page_pic_real_url_list(url : str):

    one_page_pic_real_url_list = []

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
    }

    res = requests.get(url, headers=header)

    html = res.text

    soup = BeautifulSoup(html, "html.parser")

    div_list = soup.find_all(
        name="a",
        attrs={
            "class": "entry-thumbnail"
        }
    )

    for one in div_list:
        pic_url = one.get('href')
        one_page_pic_real_url_list.append(pic_url)

    return one_page_pic_real_url_list

def get_one_thumbnail_pic_url_list(url : str):
    one_thumbnail_pic_url_list = []

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
    }

    response = requests.get(url, headers=header)

    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    src_list = soup.find(
        name="div",
        attrs={
            "class": "entry-content"
        }).find_all(
        name="img")

    for one in src_list:
        one_thumbnail_pic_url_list.append(one.get("src"))

    return one_thumbnail_pic_url_list

def download_pic_from_url(url : str):
    pic = requests.get(url)
    img = pic.content
    pic_name = url[-36:-4]
    with open('pict/'+pic_name + '.jpg', 'wb') as f:
        f.write(img)
        f.close()

if __name__ == '__main__':
    for i in tqdm(range(129)):
        url = "https://www.kanxiaojiejie.com/page/"+str(i+1)
        one_page_pic_real_url_list = get_one_page_pic_real_url_list(url)
        for one_url in tqdm(one_page_pic_real_url_list):
            one_thumbnail_pic_url_list = get_one_thumbnail_pic_url_list(one_url)
            for pic_url in one_thumbnail_pic_url_list:
                download_pic_from_url(pic_url)
        print(f"第{i+1}页爬取完成")

    print("全部爬取完成...")




