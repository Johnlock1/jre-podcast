import os
import sys
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

        path = os.path.realpath(__file__).replace(
            os.path.basename(__file__), '')
        if not os.path.exists(path + filename):
            self.podcasts = {}
        else:
            with open(filename, 'r', encoding='utf-8') as f:
                try:
                    self.podcasts = json.load(f)
                except Exception as e:
                    print(e)

    def pages(self):
        """
        Return the number of pages.
        In case of Exception, arbitrary return 200
        """
        try:
            response = requests.get('http://podcasts.joerogan.net/podcasts/')
            tree = lxml.html.fromstring(response.text)
            return int(tree.cssselect(selector['pages'])[0].text) + 1
        except:

            return 200

    def scrap_page(self, url):
        try:
            response = requests.get(url)
            tree = lxml.html.fromstring(response.text)
            return tree.cssselect(selector['podcasts'])[0]
        except:
            self.output()

    def scrap_episode(self, html):
        p = Podcast()
        p.from_html(html)
        self.add(p)

    def add(self, p):
        # if p.num in self.podcasts:
        # print(f"True {p.num}")
        # else:
        # print(f"False {p.num}")
        self.podcasts[p.num] = p.date_formated(frm2='%y.%m.%d'), p.date_formated(
            frm2='%B %d, %Y'), p.title, p.guests, p.description, p.link

    def sort_podcasts(self, reverse=True):
        self.podcasts = {k: v for k, v in sorted(
            self.podcasts.items(), key=lambda item: item[1][0], reverse=reverse)}

    def output(self):
        self.sort_podcasts()
        with open(self.filename, 'w') as f:
            json.dump(self.podcasts, f)


if __name__ == '__main__':

    scpr = Scraper()
    scpr.set_IO_file('podcasts-1.json')

    # Pass number of pages to scrap as shell argurment
    # If else scrap all available pages
    if len(sys.argv) > 2:
        sys.exit("Usage: python scrap.py [pages]")
    pages = int(sys.argv[1]) + \
        1 if len(sys.argv) == 2 else scpr.pages()

    # Scrap pages, one by one
    for page in range(1, pages):
        print(f'- Page: {page} -')

        url = f'http://podcasts.joerogan.net/podcasts/page/{page}?load'
        page_tree = scpr.scrap_page(url)

        for e in range(1, 11):
            try:
                scpr.scrap_episode(page_tree[e])
            except IndexError:
                break

    scpr.output()
