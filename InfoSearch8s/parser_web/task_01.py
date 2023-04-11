import requests
from bs4 import BeautifulSoup
import os


INIT_LINK = 'https://genius.com/tags/country/all?page='
COUNT = 100
INDEX_FILE = 'index.txt'


def get_links(url):
    page = requests.get(url)
    data = BeautifulSoup(page.text, "lxml")
    all_links = []
    for c_link in data.select("a.song_link"):
        all_links.append(c_link['href'])
    return all_links


def crawler(url):
    page = requests.get(url)
    data = BeautifulSoup(page.text, "html.parser")
    for d in data(['style', 'script', 'noscript', 'link']):
        d.decompose()
    return str(data)


if __name__ == "__main__":

    links = []
    i = 1
    info = ""
    
    while len(links) < COUNT:
        cur_link = f'{INIT_LINK}{i}'
        n_links = get_links(cur_link)
        links += n_links
        i += 1
    
    for i, link in enumerate(links):

        html_text = crawler(link)
        filename = f'00{i + 1}' if i < 9 else f'0{i + 1}' if i < 99 else '100'
        info += f'{filename}\t{link}\n'
        path_result = f"output/{filename}.txt"

        os.makedirs(os.path.dirname(path_result), exist_ok=True)
        with open(path_result, "w", encoding="utf-8") as file_result:
            file_result.write(html_text)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(info)
