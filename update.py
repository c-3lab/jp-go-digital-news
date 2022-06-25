#!/usr/bin/env python3

import csv
import datetime
import re
import requests
import shutil
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

verbose = False

def get(url, url_prefix, encoding):

    today = datetime.date.today().strftime('%Y/%m/%d')

    links = []

    res = None
    headers = { 'Cache-Control': 'no-cache' }
    try:
        res = requests.get(url, headers=headers)
    except Exception as e:
        print(f'Failed to fetch {url}', file=sys.stderr)
        return []

    if res.status_code == 403:
        try:
            headers.update({ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' })
            res = requests.get(link, headers=headers)
        except Exception as e:
            print(f'Failed to fetch {url} ({res.status_code})', file=sys.stderr)
            return []
    elif res.status_code >= 400:
            print(f'Failed to fetch {url} ({res.status_code})', file=sys.stderr)
            return []

    bs = BeautifulSoup(res.content, 'html.parser')
    for t in bs.find_all('a'):
        ref = t.get('href')
        if ref is not None:
            ref = ''.join(filter(lambda c: c >= ' ', ref))
            ref = re.sub('<.*?>', '', ref)
            ref = ref.strip()

            ref_lower = ref.lower()
            if ref_lower.startswith('#'):
                pass
            elif ref_lower.startswith('mailto:'):
                pass
            elif ref_lower.startswith('tel:'):
                pass
            elif ref_lower.startswith('javascript:'):
                pass
            elif ref.startswith(url_prefix) is False:
                pass
            else:
                ref = urljoin(url, ref)
                cs = t.strings
                if cs is None:
                    title = ''
                else:
                    title = re.sub('[　 ]+', ' ', '::'.join(filter(lambda x: len(x) > 0 and x != 'ニュース' and re.fullmatch('[0-9]+年[0-9]+月[0-9]+日', x) is None, [s.strip() for s in cs])))

                links.append([today, ref, title])
                if verbose:
                    print(f'Found {ref}: {title}', file=sys.stderr)

    return links

def search(links, data):

    result = []

    for l in links:
        for d in data:
            if l[1] == d[1] or l[2] == d[2]:
                if verbose:
                    print(f'Skip {l[1]}', file=sys.stderr)
                break
        else:
            for r in result:
                if l[1] == r[1] or l[2] == r[2]:
                    if verbose:
                        print(f'Skip {l[1]}', file=sys.stderr)
                    break
            else:
                print(f'Register {l}', file=sys.stderr)
                result.append(l)

    return result

def update(url, url_prefix, csv_path, url_encoding, csv_encoding):

    with open(csv_path, encoding=csv_encoding) as fd:
        reader = csv.reader(fd)
        data = [row for row in reader]
        print(f'Found {len(data)} records', file=sys.stderr)

    new_data = search(get(url, url_prefix, url_encoding), data)

    shutil.copy2(f'{csv_path}', f'{csv_path}.new')
    with open(f'{csv_path}.new', 'a') as fd:
        writer = csv.writer(fd, lineterminator='\n')
        writer.writerows(new_data)
        print(f'Extend to {len(data) + len(new_data)} records', file=sys.stderr)

    return 0

if __name__ == '__main__':
    x = 0
    x = x + update('https://www.digital.go.jp/councils/', 'https://www.digital.go.jp/councils/', 'jp-go-digital-news-meeting.csv', 'utf-8', 'utf-8')
    x = x + update('https://www.digital.go.jp/news/topics/', 'https://www.digital.go.jp/posts/', 'jp-go-digital-news-news.csv', 'utf-8', 'utf-8')
    exit(x)
