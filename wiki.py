import json

from podcast import Podcast

table_start = '{| class="wikitable collapsible collapsed"\n \
|-\n \
! Episode\n \
! Date\n \
! Title\n'

table_end = '|}'


def read_json():
    with open('podcasts.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

def table_build(data):
    keys = data.keys
    count = 0
    table_content = ''
    while (count < 2):
        for key in keys():
            p = Podcast()
            p.from_json_file(key, data[key])
            table_content += p.wiki_entry()
            count += 1

    return table_content







data = read_json()
table_content = table_build(data)
table = table_start + table_content + table_end

with open('table.txt', 'w', encoding='utf-8') as f:
    f.write(table)
