from config import selector


class Podcast:

    def __init__(self, tree):
        self.tree = tree
        self.num = self.extract(selector['num'])
        self.date = self.extract(selector['date'])
        self.title = self.extract(selector['title'])
        self.link = self.extract_link()
        # self.p()

    def extract(self, selector):
        return self.tree.cssselect(selector)[0].text_content()

    def extract_link(self):
        return self.tree.cssselect(selector['link'])[0].get('href')

    def p(self):
        print('num: ' + self.num)
        print('date: ' + self.date)
        print('title: ' + self.title)
        print('link: ' + self.link)
