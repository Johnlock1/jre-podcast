import json

from podcast import Podcast

table_start = '{| class="wikitable collapsible collapsed"\n \
|-\n \
! Episode\n \
! Date\n \
! Title\n \
! Guests\n \
! Description\n \
! Link\n'

table_end = '|}\n'


def read_json():
    with open('podcasts.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data


def guests_f(list):
    try:
        o = ''
        for guest in list:
            o = o + f'[[{guest}]], '
        return o[:-2]
    except:
        return ''


def wiki_entry(p):
    table = 'Master'  # title_formated()[0]
    episode = f'| {p.num}\n'
    date = f'| {p.date}\n'
    title = f'| {p.title}\n'
    guests = f'| {guests_f(p.guests)}\n'
    description = f'| {p.description}\n'
    link = f'| {{{{small|{p.link}}}}} \n'  # output: {{small|link}}
    return (table, f'|- \n {episode} {date} {title} {guests} {description} {link}')


def year(podcast):
    return int(podcast.date[-4:])


def last_year(data):
    key = list(data.keys())[0]
    p = Podcast()
    p.from_json_file(key, data[key])
    return year(p)


def interim_table(body, year):
    return f'=={year} Episodes ==\n' + table_start + body + table_end + '\n'


def table_build(data):
    keys = data.keys
    count = 0
    table = ''
    master_body = ''
    # flight_content = ''
    # mma_content = ''
    # regural_content = ''

    latest_year = last_year(data)

    for key in keys():
        p = Podcast()
        p.from_json_file(key, data[key])

        if (year(p)) < latest_year:
            table += interim_table(master_body, latest_year)
            latest_year -= 1
            master_body = ''

        table_content = wiki_entry(p)
        # print(table_content)
        if table_content[0] == 'Master':
            master_body += table_content[1]
        # if table_content[0] == 'Fight':
        #     flight_content += table_content[1]
        # elif table_content[0] == 'MMA':
        #     mma_content += table_content[1]
        # else:
        #     regural_content += table_content[1]

    return table  # flight_content, mma_content, regural_content


data = read_json()

# flight_content, mma_content, regural_content = table_build(data)
master_table = table_build(data)

# flight_table = table_start + flight_content + table_end
# mma_table = table_start + mma_content + table_end
# regural_table = table_start + regural_content + table_end

with open('table.txt', 'w+', encoding='utf-8') as f:
    f.write('{{User sandbox}}\n<!-- EDIT BELOW THIS LINE -->\n\n')
    f.write(master_table)
    # f.write('== Fight Companion ==\n')
    # f.write(flight_table)
    # f.write('== MMA Show ==\n')
    # f.write(mma_table)
    # f.write('== Regular Episodes ==\n')
    # f.write(regural_table)
