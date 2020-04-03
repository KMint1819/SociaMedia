from requests_html import HTMLSession
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom


class Crawler(object):
    ROOT = 'https://www.reddit.com'

    def __init__(self):
        self.session = HTMLSession()

    @staticmethod
    def get_title(html):
        post_content = html.find('div[data-test-id=post-content]', first=True)
        divs = post_content.find('div')
        return divs[11].text

    @staticmethod
    def get_content(html):
        post_content = html.find('div[data-test-id=post-content]', first=True)
        divs = post_content.find('div')
        return divs[14].text

    @staticmethod
    def get_comments(html, num=3):
        com_elements = html.find('div[data-test-id=comment]')
        # print(f'Comment numbers: {len(com_elements)}')
        result = []
        for com_element in com_elements:
            if len(result) == num:
                break
            divs = com_element.find('div')
            result.append(divs[1].text)

        return result

    def get_page_content(self, url):
        print('Getting page: ', url)
        r = self.session.get(url)
        title = self.get_title(r.html)
        content = self.get_content(r.html)
        comments = self.get_comments(r.html)
        print(f'Title:\n{title}')
        print('-' * 50)
        print(f'Content:\n{content}')

        print('-' * 50)
        print(f'Comments:')
        for i, comment in enumerate(comments):
            print(f'Comment{i}: {comment}')
        print('='*50)
        print('='*50)
        print('='*50)
        return title, content, comments

    def execute(self, board_url, page_num=3):
        r = self.session.get(board_url)
        soup = BeautifulSoup(r.text, 'lxml')
        ass = soup.find_all('a', {'class': '_2INHSNB8V5eaWp4P0rY_mE'})
        result = []
        for a in ass:
            if len(result) == page_num:
                break
            url = f'{self.ROOT}{a.attrs["href"]}'
            page_content = self.get_page_content(url)
            result.append(page_content)
        return result

def test():
    url = 'https://www.reddit.com/r/learnjava/comments/ftkpls/how_good_is_caleb_curry_to_learn_java_from/'
    crawler = Crawler()
    crawler.get_page_content(url)

def main(query):
    board_url = f'https://www.reddit.com/search/?q={query}'
    crawler = Crawler()
    posts = crawler.execute(board_url)
    xml_root = ET.Element('xml')
    for post in posts:
        xml_post = ET.SubElement(xml_root, 'post')
        xml_title = ET.SubElement(xml_post, 'title')
        xml_content = ET.SubElement(xml_post, 'content')
        xml_comments = []
        for i in range(len(post[2])):
            xml_comments.append(ET.SubElement(xml_post, 'comment'))

        xml_title.text = post[0]
        xml_content.text = post[1]
        for i, xml_comment in enumerate(xml_comments):
            xml_comment.text = post[2][i]

    xmlstr = minidom.parseString(ET.tostring(xml_root)).toprettyxml(indent="   ")
    with open('result.xml', 'w+') as f:
        f.write(xmlstr)


if __name__ == "__main__":
    main('samsung')
    # test()
    # Crawler().execute()
