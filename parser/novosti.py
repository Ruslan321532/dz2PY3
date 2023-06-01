import requests
from bs4 import BeautifulSoup


URL="https://demirbank.kg/ru/about/news/index"
HEADERS={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}
#GET, POST, DELETE, PATCH
def get_html(url):
    response = requests.get(url, headers=HEADERS)
    return response


def get_data(html):
    soup = BeautifulSoup(html,'html.parser')
    items = soup.find_all("article", class_="timeline-box left post post-medium")
    parsed_data = []
    http = "https://demirbank.kg/ru"
    for item in items:
        parsed_data.append({
            "title": item.find("h4", class_="heading-primary").find('a').get_text(),
            "url": http + item.find("h4", class_="heading-primary").find('a').get('href'),
            "date": item.find("div", class_="post-meta").find('span').get_text(),
            "img": http + item.find("img", class_="img-responsive").get('src')
        })
    return parsed_data


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        parsed_data = get_data(html.text)
        return parsed_data
    raise Exception("Ошибка в парсере!")




