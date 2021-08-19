import unicodedata
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

# <함수 모음>-----------------------------------------------------------
def insta_searching(word):
    url = f'https://www.instagram.com/explore/tags/{word}'
    return url

def select_first(driver):
    first = driver.find_element_by_css_selector('div._9AhH0')
    first.click()
    time.sleep(3)

def get_content(driver):
    # 현재 페이지의 html 정보 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 본문내용 가져오기
    try:
        content = soup.select_one('div.C4VMK > span').text
        content = unicodedata.normalize('NFC', content)
    except:
        content = ''

    # 본문내용에서 해시태그 가져오기
    tags = re.findall(r'#[^\s#,\\]+', content)

    # 작성일자 정보 가져오기
    date = soup.select_one('time._1o9PC.Nzb55')['datetime'][:10]

    # 조회 수 가져오기
    try:
        views = soup.select_one('span.vcOH2').text[3:-1]
    except:
        views = 0

    # 위치정보 가져오기
    try:
        place = soup.select_one('div.M30cS')[0].text
        place = unicodedata.normalize('NFC', place)
    except:
        place = ''

    data = [date, views, place, tags]

    return data

def move_next(driver):
    go_to_right_button = driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow')
    go_to_right_button.click()
    time.sleep(3)

# <크롬 브라우저 열기>---------------------------------------------------
driver = webdriver.Chrome('./chromedriver.exe')
insta_url = 'https://www.instagram.com'
driver.get(insta_url)
time.sleep(2)

# <로그인 과정 진행>--------------------------------
# 계정 입력
acc = 'kim_yh663927@naver.com'
input_email = driver.find_element_by_css_selector('input._2hvTZ.pexuQ.zyHYP')
print(input_email)
input_email.clear()
input_email.send_keys(acc)

# pwd 입력
with open('./password.txt') as f:
    password = f.read(14)
input_pwd = driver.find_element_by_name('password')
input_pwd.clear()
input_pwd.send_keys(password)
input_pwd.submit()
time.sleep(3)

# 나중에 하기 누르기
try:
    driver.find_element_by_css_selector('.sqdOP.yWX7d.y3zKF').click()
    time.sleep(3)
    print(1)
except:
    pass
try:
    driver.find_element_by_css_selector('.aOOlW.HoLwm').click()
    time.sleep(1)
except:
    pass

# 검색 페이지 url 만들기
word = '제주도맛집'
url = insta_searching(word)
driver.get(url)
time.sleep(5)

# 첫번째 게시글 열기
select_first(driver)

# 500개 게시글 정보 수집
results = []
target = 50

for i in range(target):
    try:
        # 게시글 데이터 수집
        data = get_content(driver)
        results.append(data)
        move_next(driver)
    except:
        # 오류발생시 다음 페이지
        time.sleep(2)
        move_next(driver)

df = pd.DataFrame(
    results, columns=['게시일자', '조회수', '주소', '해시태그']
)
print(df.head())
df.to_csv('instagram.csv', encoding='utf-8-sig')
exit()

