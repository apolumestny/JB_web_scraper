from __future__ import annotations
import os
import requests
import string

from bs4 import BeautifulSoup


def save_article(page: str, type: str) -> None:
    for page_num in range(1, int(page) + 1):
        # create directory
        if not os.path.exists(f'Page_{str(page_num)}'):
            os.mkdir(f'Page_{str(page_num)}')
        url: str = f'https://www.nature.com/nature/articles?page={page_num}'
        headers: dict = {'Accept-Language': 'en-US,en;q=0.5'}
        r: requests.Response = requests.get(url, headers=headers)
        soup: BeautifulSoup = BeautifulSoup(r.content, 'html.parser')
        article = soup.find_all('article')
        for topic in article:
            if topic.find('span', {'class': 'c-meta__type'}).text == type:
                relative_url: str = topic.find('a', {'class': 'c-card__link u-link-inherit'}, href=True)['href']
                absolute_url: str = f'https://www.nature.com{relative_url}'
                sub_r: requests.Response = requests.get(absolute_url, headers=headers)
                if sub_r.status_code != requests.codes.ok:
                    return print(f'The URL returned {r.status_code}')
                topic_soup: BeautifulSoup = BeautifulSoup(sub_r.content, 'html.parser')
                file_name: str = topic_soup.find('h1', {'class': 'c-article-magazine-title'}).text
                translator = str.maketrans('', '', string.punctuation)
                file_name = file_name.translate(translator).replace(' ', '_').strip()
                file_content: str = topic_soup.find('div', {'class': 'c-article-body u-clearfix'}).text.strip()
                with open(os.path.join(f'Page_{page_num}', f'{file_name}.txt'), 'w') as file:
                    file.write(file_content)


if __name__ == '__main__':
    page_count: str = input()
    type: str = input()
    save_article(type=type, page=page_count)
