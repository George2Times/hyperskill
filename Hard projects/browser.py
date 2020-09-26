import argparse
import os
import requests

from colorama import Fore
from bs4 import BeautifulSoup
from collections import deque


class TextBasedBrowser:
    commands = {'exit', 'back'}
    html_tags = ['div', 'script', 'p',
                 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                 'a', 'ul', 'ol', 'li']
    prompt = "'url') Print web page content\n" + \
             "'page name') Print web page content that was already visited\n" + \
             "'exit') Ends the program\n" + \
             "'back') Get least visited page\n"

    def __init__(self, name='browser', saved_pages_dir='temp'):
        self.name = name
        self.history_dir = saved_pages_dir
        if not os.path.exists(self.history_dir):
            os.makedirs(name=self.history_dir)

        self.soup = ''
        self.history = deque()
        self.current_page = ''

        self.running = True
        self.main_loop()

    def _to_file_path(self, string: str) -> str:
        """
        string: google.com          -> {self.history_dir}/google.txt
        string: google.txt          -> {self.history_dir}/google.txt
        string: google.ffd21x.fd    -> {self.history_dir}/google.txt
        """
        file_name = string[string.find('//'):string.find('.')]
        return self.history_dir + '/' + file_name + '.txt'

    def save_page_to_file(self, url: str, page_data: str) -> None:
        file_path = self._to_file_path(url)
        with open(file_path, "w", encoding='UTF-8') as f:
            f.write(page_data)

    def search_for_file(self, page_name: str) -> str:
        try:
            file_path = self._to_file_path(page_name)
            with open(file_path, "r", encoding='UTF-8') as f:
                return f.read()
        except FileNotFoundError:
            return 'Error: FileNotFoundError'

    def get_readable_page(self, page_text: str) -> str:
        self.soup = BeautifulSoup(page_text, 'html.parser')
        # Fore.BLUE +
        result = []
        for tag in self.soup.find_all('a'):
            if tag.name == 'a':
                result.append(tag.text)
            else:
                result.append(tag.text)
        return'\n'.join(result)

    @staticmethod
    def check_url(site: str) -> str:
        """
        google.com          -> https://google.com
        https://google.com  -> https://google.com
        """
        return site if site.startswith("https://") else "https://" + site

    @staticmethod
    def request_get_page_text(url: str) -> str:
        req = requests.get(url)
        req.encoding = 'utf-8'
        return req.text

    def load_page(self, url: str) -> str:
        if url == '':
            return ''
        else:
            result = self.request_get_page_text(self.check_url(url))
            if result != 'Error: Incorrect URL':
                result = self.get_readable_page(result)

                # add to history
                if self.current_page != '':
                    self.history.appendleft(self.current_page)
                self.current_page = url

                self.save_page_to_file(url=url, page_data=result)
        return result

    @staticmethod
    def is_valid_url(url: str) -> bool:
        return True if url.find('.') != -1 else False

    def load_page_from_history(self) -> str:
        try:
            last = self.history.pop()
            data = self.search_for_file(page_name=last)
            if data != 'Error: FileNotFoundError':
                return data
            else:
                return ''
        except IndexError:
            return ''

    def shutdown(self) -> None:
        self.running = False

    def main_loop(self) -> None:
        """
        lambda: None defines a function that does nothing, as such,
        if wrong input was entered, it would print 'Error: Incorrect URL'
        """
        while self.running:
            choice = input()
            if choice == 'exit':  # terminate loop
                self.shutdown()
            elif choice == 'back':  # last page from history
                print(self.load_page_from_history())
            elif self.is_valid_url(choice):  # browse the page
                print(Fore.BLUE + self.load_page(url=choice))
            else:
                result = self.search_for_file(page_name=choice)
                print('Error: Incorrect URL' if result == 'Error: FileNotFoundError'
                      else Fore.BLUE + result)


def main():
    parser = argparse.ArgumentParser(description='Text based web browser')
    parser.add_argument('saved_pages_dir', type=str, default='temp',
                        help='enter directory where browsed pages will be saved')
    args = parser.parse_args()

    TextBasedBrowser(saved_pages_dir=args.saved_pages_dir)


if __name__ == '__main__':
    main()