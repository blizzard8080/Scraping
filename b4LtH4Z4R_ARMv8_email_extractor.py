#!/usr/bin/python3/env
#Scraping by Giscard Salindeho a.k.a b4LtH4Z4R_ARMv8
#IG @blizzard8080
#Email Scraping

from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re


masukan_url = str(input('[+] Masukan Target URL:'))
urls = deque([masukan_url])

terget_x_url = set()
emails = set()
user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

count = 0
try:
    while len(urls):
        count += 1
        if count == 100:
            break
        url = urls.popleft()
        terget_x_url.add(url)

        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)

        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        print('[%d] Sedang Proses %s' % (count, url))
        try:
            respone = requests.get(url, headers=user_agent)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", respone.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(respone.text, features="lxml")

        for anchor in soup.find_all("a"):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link in urls and not link in masukan_url:
                urls.append(link)

except KeyboardInterrupt:
        print('[-] Selesai BOS!!')

for mail in emails:
    print(mail)
