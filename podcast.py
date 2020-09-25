import re
from datetime import datetime

from config import selector


class Podcast:

    def __init__(self):
        pass

    def from_html(self, html):
        self.html = html
        self.num = html.find_class('episode-num')[0].text_content()
        self.date = html.cssselect(selector['date'])[0].text
        thumb = html.cssselect(selector['thumbnail'])[0]
        self.title = thumb.items()[3][1]
        self.link = thumb.items()[1][1]
        self.description = self._description()
        self.guests = self._guests()

    def from_json_file(self, key, value):
        self.num = key
        self.date = value[1]
        self.title = value[2]
        self.guests = value[3]
        self.description = value[4]
        self.link = value[5]

    def _guests(self):
        guests = []
        for i in range(20):
            try:
                guest = self.html.cssselect(
                    f'div.podcast-content > strong:nth-child({i})')[0].text
                if guest not in ('', ' '):
                    guests.append(guest)
            except IndexError as e:
                pass

        if len(guests) != 0:
            return guests
        else:
            return None

    def _description(self):
        desc = self.html.cssselect(selector['content'])[0].text_content()

        if desc != '':
            return desc.split(".")[1].lstrip()
        else:
            return None

    def date_type(self, frm1='%m.%d.%y'):
        return datetime.strptime(self.date, frm1)

    def date_formated(self, frm1='%m.%d.%y', frm2='%Y %b %d'):
        return datetime.strptime(self.date, frm1).strftime(frm2)

    def title_formated(self):
        regex = ' with | & |, '
        t = ''

        if self.title[:5] == 'Fight':
            return ('Fight', self.title)
        guests = re.split(regex, self.title)
        l = len(guests)
        for i, g in enumerate(guests):
            if i == 0 and g[:3] in ['MMA', 'JRE']:
                t += f'{g}'
                if i < l - 1:
                    t += ' with '
            else:
                t += f'[[{g}]]'
                if i < l - 1:
                    t += ', '
        t + '\n'
        if t[:3] in ['MMA', 'JRE']:
            return ('MMA', t)
        return ('Regular', t)

    def p(self):
        print('num: ' + self.num)
        print('date: ' + self.date)
        print('title: ' + self.title)
        print('link: ' + self.link)
