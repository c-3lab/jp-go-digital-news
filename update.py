#!/usr/bin/env python3

import csv
import datetime
import pathlib
import os
import re
import requests
import shutil
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get(url, site_group_lower=[]):

    today = datetime.date.today().strftime('%Y/%m/%d')

    links = []

    res = None
    headers = { 'Cache-Control': 'no-cache' }
    try:
        res = requests.get(url, headers=headers)
    except Exception as e:
        print(f'Failed to fetch {url}', file=sys.stderr)
        print(f'Exception {e}', file=sys.stderr)
        return None

    if res.status_code == 403:
        try:
            headers.update({ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' })
            res = requests.get(link, headers=headers)
        except Exception as e:
            print(f'Failed to fetch {url} ({res.status_code})', file=sys.stderr)
            return None
    elif res.status_code >= 400:
            print(f'Failed to fetch {url} ({res.status_code})', file=sys.stderr)
            return None

    bs = BeautifulSoup(res.content, 'html.parser')
    for t in bs.find_all('a'):
        ref = t.get('href')
        if ref is not None:
            ref = ''.join(filter(lambda c: c >= ' ', ref))
            ref = re.sub('<.*?>', '', ref)
            ref = ref.strip()

            title = None

            ref_lower = ref.lower()
            if ref_lower.startswith('#'):
                pass
            elif ref_lower.startswith('mailto:'):
                pass
            elif ref_lower.startswith('tel:'):
                pass
            elif ref_lower.startswith('javascript:'):
                pass
            elif len(site_group_lower) > 0:
                for site_lower in site_group_lower:
                    if ref_lower.startswith(site_lower):
                        title = '::'.join([s.strip() for s in t.strings])
            elif len(t.find_all('h3')) > 0:
                cs = t.strings
                if cs is None:
                    title = ''
                else:
                    title = re.sub('[　 ]+', ' ', '::'.join(filter(lambda x: len(x) > 0 and x != 'ニュース' and re.fullmatch('[0-9]+年[0-9]+月[0-9]+日', x) is None, [s.strip() for s in cs])))

            if title is None or len(title) == 0: # jump to last page
                pass
            elif re.fullmatch('[0-9]+', title): # jump to page number
                pass
            else:
                ref_full = urljoin(url, ref)
                links.append([today, ref_full, title])

    print(f'Remote: Found {len(links)} links', file=sys.stderr)
    return links

def search(links, data):

    result = []

    for l in links:
        for d in data:
            if l[1] == d[1] or l[2] == d[2]:
                break
        else:
            for r in result:
                if l[1] == r[1] or l[2] == r[2]:
                    break
            else:
                print(f'Remote: Registering {l}', file=sys.stderr)
                result.append(l)

    print(f'Remote: Found {len(result)} new links', file=sys.stderr)
    return result

def update(url, csv_path, csv_encoding, site_group=[]):

    site_group_lower = []
    for site in site_group:
        site_group_lower.append(site.lower())

    print(f'-------- {csv_path} --------', file=sys.stderr)

    data = []
    if os.path.isfile(csv_path):
        with open(csv_path, encoding=csv_encoding) as fd:
            reader = csv.reader(fd)
            data = [row for row in reader]
            print(f'{csv_path}: Found {len(data)} records', file=sys.stderr)
    else:
        pathlib.Path(csv_path).touch()
        print(f'{csv_path}: New file', file=sys.stderr)

    links = get(url, site_group_lower=site_group_lower)
    if links is None:
        return 1

    new_data = search(links, data)
    if len(new_data) > 0:
        shutil.copy2(f'{csv_path}', f'{csv_path}.new')
        with open(f'{csv_path}.new', 'a') as fd:
            writer = csv.writer(fd, lineterminator='\n')
            writer.writerows(new_data)
            print(f'{csv_path}: Stored new {len(new_data)} records', file=sys.stderr)
        shutil.move(f'{csv_path}.new', f'{csv_path}')

    return 0

if __name__ == '__main__':
    x_all = 0
    x_all = x_all + update('https://www.digital.go.jp/councils/', 'jp-go-digital-news-meeting.csv', 'utf-8')
    x_all = x_all + update('https://www.digital.go.jp/news/', 'jp-go-digital-news-news.csv', 'utf-8')
    x_prev = -1
    x_prev2 = -1
    for i in range(2, 20):
        x = update('https://www.digital.go.jp/news/' + str(i) + '/', 'jp-go-digital-news-news.csv', 'utf-8')
        x_prev2 = x_prev
        x_prev = x
        x_all = x_all + x
        if x_prev2 == 0 and x_prev == 0:
            break
    x_all = x_all + update('https://www.digital.go.jp/procurement/', 'jp-go-digital-news-procurement.csv', 'utf-8',
                           site_group=['https://www.p-portal.go.jp/'])
    exit(x)
