import json

from podcast import Podcast

table_start = '{| class="wikitable collapsible collapsed"\n \
|-\n \
! Episode\n \
! Date\n \
! Title\n'

table_end = '|}\n'


def read_json():
    with open('podcasts.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

def table_build(data):
    keys = data.keys
    count = 0
    flight_content = ''
    mma_content = ''
    regural_content = ''
    while (count < 2):
        for key in keys():
            p = Podcast()
            p.from_json_file(key, data[key])
            table_content = p.wiki_entry()
            # print(table_content)
            if table_content[0] == 'Fight':
                flight_content += table_content[1]
            elif table_content[0] == 'MMA':
                mma_content += table_content[1]
            else:
                regural_content += table_content[1]

            count += 1

    return flight_content, mma_content, regural_content




data = read_json()
flight_content, mma_content, regural_content = table_build(data)

flight_table = table_start + flight_content + table_end
# print(flight_table)
mma_table = table_start + mma_content + table_end
regural_table = table_start + regural_content + table_end

with open('table.txt', 'w+', encoding='utf-8') as f:
    f.write(flight_table)
    f.write(mma_table)
    f.write(regural_table)
