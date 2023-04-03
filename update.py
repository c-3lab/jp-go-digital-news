#!/usr/bin/env python3

import csv
import datetime
import json
import pathlib
import os
import re
import requests
import shutil
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get(url, news=False, site_group_lower=[]):

    url_lower = url.lower()
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

        section = t.find_parent('section')
        if section:
            cls = section.get('class')
        else:
            cls = None
        if (news is False and section is not None) or (news is True and section is None):
            continue

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
            elif len(site_group_lower) > 0 and len(list(filter(lambda x: x.name == 'li', t.parents))) > 0:
                for site_lower in site_group_lower:
                    if ref_lower.startswith(site_lower):
                        title = '::'.join([s.strip() for s in t.strings])
            elif len(t.find_all('h3')) > 0:
                cs = t.strings
                if cs:
                    title = re.sub('[　 ]+', ' ', '::'.join(filter(lambda x: len(x) > 0 and x != 'ニュース' and re.fullmatch('[0-9]+年[0-9]+月[0-9]+日', x) is None, [s.strip() for s in cs])))

            if title is None or len(title) == 0: # jump to last page
                pass
            elif re.fullmatch('[0-9]+', title): # jump to page number
                pass
            else:
                ref_full = urljoin(url, ref)

                dt = today
                tm = t.find('time')
                if tm:
                    dt = ''.join(tm.strings)
                    if dt:
                        dt = dt.replace('年', '/')
                        dt = dt.replace('月', '/')
                        dt = dt.replace('日', '')

                links.append([dt, ref_full, title])

    print(f'Remote: Found {len(links)} links', file=sys.stderr)
    return links

def search(links, data):

    result = []

    for l in links:
        for d in data:
            if l[1] == d[1] and l[2] == d[2]:
                break
        else:
            for r in result:
                if l[1] == r[1] and l[2] == r[2]:
                    break
            else:
                print(f'Remote: Registering {l}', file=sys.stderr)
                result.append(l)

    print(f'Remote: Found {len(result)} new links', file=sys.stderr)
    return result

def update(url, csv_path, csv_encoding, news=False, site_group=[]):

    site_group_lower = []
    for site in site_group:
        site_group_lower.append(site.lower())

    print(f'-------- {url} --------', file=sys.stderr)

    data = []
    if os.path.isfile(csv_path):
        with open(csv_path, encoding=csv_encoding) as fd:
            reader = csv.reader(fd)
            data = [row for row in reader]
            print(f'{csv_path}: Found {len(data)} records', file=sys.stderr)
    else:
        pathlib.Path(csv_path).touch()
        print(f'{csv_path}: New file', file=sys.stderr)

    links = get(url, news=news, site_group_lower=site_group_lower)
    if links is None:
        return -1

    new_data = search(links, data)
    updated = len(new_data)
    if updated > 0:
        shutil.copy2(f'{csv_path}', f'{csv_path}.new')
        with open(f'{csv_path}.new', 'a') as fd:
            writer = csv.writer(fd, lineterminator='\n')
            writer.writerows(new_data)
            print(f'{csv_path}: Stored new {updated} records', file=sys.stderr)
        shutil.move(f'{csv_path}.new', f'{csv_path}')

    return updated

if __name__ == '__main__':

    config_file_path = './jp-go-digital-news-config.json'
    with open(config_file_path) as fconfig:
        config = json.loads(fconfig.read())

    result = 0

    for site in config['sites']:
        url = site['url']
        report = site['report']
        encoding = site['encoding']
        news = site['news']
        site_group = site['sitegroup']

        x = update(url, report, encoding, news=news, site_group=site_group)
        if x < 0:
            result = 1
            continue

        if news is True:
            x_prev2 = 0
            x_prev = 0
            for i in range(2, 100):
                x = update(url + str(i) + '/', report, encoding, news=news, site_group=site_group)
                if x < 0:
                    break
                x_prev2 = x_prev
                x_prev = x
                if x_prev2 == 0 and x_prev == 0:
                    break

    exit(result)
