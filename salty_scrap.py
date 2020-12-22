import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
tr_info = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
# Python에서 strip()을 이용하면 문자열에서 특정 문자를 제거할 수 있습니다.
# Java 등의 다른 언어들도 strip()을 제공하며, 기능은 모두 비슷합니다.

# strip([chars]) : 인자로 전달된 문자를 String의 왼쪽과 오른쪽에서 제거합니다.
# lstrip([chars]) : 인자로 전달된 문자를 String의 왼쪽에서 제거합니다.
# rstrip([chars]) : 인자로 전달된 문자를 String의 오른쪽에서 제거합니다.
for tr in tr_info:
    rank = tr.select_one('td.number').text[0:2].strip()
    title = tr.select_one('td.info > a.title.ellipsis').text.strip()
    artist = tr.select_one('td.info > a.artist.ellipsis').text
    # print(rank, title, artist)
    doc = {
        'rank': rank,
        'title': title,
        'artist': artist
    }
    db.musics.insert_one(doc)
