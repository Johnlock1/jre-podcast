import requests
import lxml.html
import json
from config import selector
from podcast import Podcast

podcasts = {}

for page in range(1, 168):
    print(page, end=' ')

    url = f'http://podcasts.joerogan.net/podcasts/page/{page}?load'
    response = requests.get(url)
    tree = lxml.html.fromstring(response.text)

    podcasts_tree = tree.cssselect(selector['podcasts'])[0]

    for i in range(2, 11):
        p = Podcast(podcasts_tree[i])

        podcasts[p.num] = [p.date, p.title, p.link]

with open('podcasts.json', 'w') as f:
    json.dump(podcasts, f)
