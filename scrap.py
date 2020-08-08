import os
import requests
import lxml.html
import json
from config import selector
from podcast import Podcast


class Scraper():

    def __init__(self):
        pass

    def set_IO_file(self, filename):
        self.filename = filename

        path = os.path.realpath(__file__).replace(os.path.basename(__file__),'')
        if not os.path.exists(path+filename):
            self.podcasts = {}
        else:
            with open(filename, 'r', encoding='utf-8') as f:
                try:
                    self.podcasts = json.load(f)
                except Exception as e:
                    print(e)

    def scrap_page(self, url):
        try:
            response = requests.get(url)
            tree = lxml.html.fromstring(response.text)
            return tree.cssselect(selector['podcasts'])[0]
        except:
            self.output()

    def scrap_episode(self, html):
        p = Podcast()
        p.from_tree(html)
        self.add(p)

    def add(self, p):
        if p.num in self.podcasts:
            print(f"True {p.num}")
        else:
            print(f"False {p.num}")
            self.podcasts[p.num] = p.date_formated(frm2='%Y %m %d'), p.title, p.link

    def sort_podcasts(self, reverse=True):
            self.podcasts = {k: v for k, v in sorted(self.podcasts.items(), key=lambda item: item[1][0], reverse=reverse)}

    def output(self):
        self.sort_podcasts()
        with open(self.filename, 'w') as f:
            json.dump(self.podcasts, f)


if __name__ == '__main__':
    scpr = Scraper()
    scpr.set_IO_file('podcasts.json')

    for page in range(1, 172):
        print(f'Page: {page}')

        url = f'http://podcasts.joerogan.net/podcasts/page/{page}?load'
        page_tree = scpr.scrap_page(url)

        for e in range(1,11):
            try:
                scpr.scrap_episode(page_tree[e])
            except IndexError:
                print(0)
                break

    scpr.output()
