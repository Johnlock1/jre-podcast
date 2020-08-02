import requests
import lxml.html
import json
from config import selector
from podcast import Podcast

podcasts = {}

with open('podcasts.json', encoding='utf-8') as f:
    data = json.load(f)
    keys = data.keys()

    for page in range(1, 3): # 168
        print(f'Page: {page}')

        url = f'http://podcasts.joerogan.net/podcasts/page/{page}?load'
        response = requests.get(url)
        tree = lxml.html.fromstring(response.text)

        podcasts_tree = tree.cssselect(selector['podcasts'])[0]

        for i in range(2, 11):
            p = Podcast()
            p.from_tree(podcasts_tree[i])
            if p.num in keys:
                print(f"True {p.num}")
            else:
                print(f"False {p.num}")

                podcasts[p.num] = [p.date, p.title, p.link]
