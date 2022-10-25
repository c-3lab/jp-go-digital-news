#!/bin/env python3

# Usage: python3 ./test.py url site_group..

import os
import sys
from update import update
from urllib.parse import urlparse

if __name__ == '__main__':
    dir = 'tmp'
    os.makedirs(dir, exist_ok=True)

    if len(sys.argv) > 1:
        url = sys.argv[1]
        site_group = sys.argv[2:]

        print(url)
        urlobj = urlparse(url)
        csv = dir + '/' + urlobj.netloc + urlobj.path.replace('/', '_') + 'out.csv'
        count = update(url, csv, 'utf-8', site_group=site_group)
        print(f'{count}: {url} -> {csv}')

    exit(0)
