import requests
from bs4 import BeautifulSoup
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from unicodedata import normalize

def main():
    web_crawler()
    scrape_text()
    clean_text()
    tf_dict = extract_import_terms()
    knowledge_base = create_knowledge_base(tf_dict)
    print(knowledge_base)


def create_knowledge_base(tf_dict):
    knowledge_base = {}
    for i in range(1, 16):
        with open('text_files_out/file' + str(i) + '_out.txt', 'rb') as f:
            text = str(f.read().decode('utf-8'))
            sents = sent_tokenize(text)
            for sent in sents:
                for key in tf_dict.keys():
                    if key in sent:
                        if key in knowledge_base:
                            knowledge_base[key].append(sent)
                        else:
                            knowledge_base[key] = [sent]
    return knowledge_base


def extract_import_terms():
    tf_dict = {}
    for i in range(1, 2):
        with open('text_files_out/file' + str(i) + '_out.txt', 'rb') as f:
            text = str(f.read().decode('utf-8'))
            text = text.lower()
            tokens = word_tokenize(text)
            stop_words = set(stopwords.words('english'))
            tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
            for t in tokens:
                if t in tf_dict:
                    tf_dict[t] += 1
                else:
                    tf_dict[t] = 1

    keys = list(tf_dict.keys())
    values = list(tf_dict.values())
    sorted_value_index = np.argsort(values)[::-1]
    sorted_tf_dict = {keys[i]: values[i] for i in sorted_value_index}
    num = 0
    for key in sorted_tf_dict:
        if num == 40:
            break
        print(str(num+1) + '. ' + key + ': ' + str(sorted_tf_dict[key]))
        num += 1
    return sorted_tf_dict


def clean_text():
    for i in range(1, 16):
        with open('text_files_in/file' + str(i) + '_in.txt', 'rb') as f:
            text = str(f.read().decode('utf-8'))
            file = open('text_files_out/file' + str(i) + '_out.txt', 'wb')
            text_holder = text.split('\n')
            valuable_text = []
            for item in text_holder:
                if item == '':
                    continue
                else:
                    if item.strip() == '':
                        continue
                    else:
                        valuable_text.append(item.strip())
            new_text = '. '.join(valuable_text)
            file.write(new_text.encode('utf-8'))


def scrape_text():
    with open('urls.txt', 'r') as f:
        urls = f.read().splitlines()
    num = 1
    for u in urls:
        page = requests.get(u, allow_redirects=False)
        soup = BeautifulSoup(page.content, 'html.parser')
        with open('text_files_in/file' + str(num) + '_in.txt', 'wb') as f:
            f.write(soup.get_text().encode('utf-8'))
        num += 1


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


def web_crawler():
    url = 'https://www.google.com/search?client=firefox-b-1-d&q=everything+everywhere+all+at+once'
    queue = [url]
    num_urls = 0

    with open('urls.txt', 'w') as f:
        while num_urls < 15:
            r = requests.get(queue.pop(0), allow_redirects=False)
            data = r.text
            soup = BeautifulSoup(data, features='lxml')
            for link in soup.find_all('a'):
                if num_urls > 14:
                    break
                link_str = str(link.get('href'))
                testing_link = link_str.lower()
                if re.search('everything.*everywhere.*all.*at.*once', testing_link):
                    if link_str.startswith('/url?q='):
                        link_str = link_str[7:]
                    if '&' in link_str:
                        i = link_str.find('&')
                        link_str = link_str[:i]
                    if link_str.startswith(
                            'http') and 'google' not in link_str and 'au' not in link_str and 'metacritic' not in link_str and 'amazon' not in link_str and 'etonline' not in link_str and 'wiki' not in link_str:
                        f.write(link_str + '\n')
                        queue.append(link_str)
                        num_urls += 1


if __name__ == "__main__":
    main()
