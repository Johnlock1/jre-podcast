import re
from datetime import datetime

from config import selector

class Podcast:

    def __init__(self):
        pass

    def from_tree(self, tree):
        self.tree = tree
        self.num = self.extract(selector['num'])
        self.date = self.extract(selector['date'])
        self.title = self.extract(selector['title'])
        self.link = self.extract_link()

    def from_json_file(self, key, value):
        self.num = key
        self.date = value[0]
        self.title = value[1]
        self.link = value[2]

    def extract(self, selector):
        return self.tree.cssselect(selector)[0].text_content()

    def extract_link(self):
        return self.tree.cssselect(selector['link'])[0].get('href')

    def date_type(self, frm1='%m.%d.%y'):
        return datetime.strptime(self.date,frm1)

    def date_formated(self, frm1='%m.%d.%y', frm2='%Y %b %d'):
        return datetime.strptime(self.date,frm1).strftime(frm2)

    def title_formated(self):
        regex = ' with | & |, '
        t = ''

        if self.title[:5] == 'Fight':
            return ('Fight', self.title + '\n')
        guests = re.split(regex, self.title)
        l = len(guests)
        for i, g in enumerate(guests):
            if i == 0 and g[:3] in ['MMA', 'JRE']:
                t += f'{g}'
                if i < l-1:
                    t += ' with '
            else:
                t += f'[[{g}]]'
                if i < l-1:
                    t += ', '
        t + '\n'
        if t[:3] in ['MMA', 'JRE']:
            return ('MMA', t)
        return ('Regular', t)



    def wiki_entry(self):
        episode = f'| {self.num}\n'
        date = f'| {self.date_formated()}\n'
        title = f'| {self.title_formated()[1]}\n'
        table = self.title_formated()[0]
        return (table, f'|- \n {episode} {date} {title}')

    def p(self):
        print('num: ' + self.num)
        print('date: ' + self.date)
        print('title: ' + self.title)
        print('link: ' + self.link)
