""" 
개발 환경 : vscode

패키지 설치 : 
- pip install pandas
- pip install selenium
- pip install bs4
- pip install lxml
- pip install openpyxl
- pip install webdriver_manager

ChromeDriver 설치 :
현재 Chrome 버전에 맞는 ChromeDriver 설치
참고 : https://dduniverse.tistory.com/entry/ChromeDriver-%EB%B2%84%EC%A0%84-%EC%98%A4%EB%A5%98-%ED%95%B4%EA%B2%B0-%EB%B0%8F-webdriver-manager-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0
설치 : https://googlechromelabs.github.io/chrome-for-testing/
버전 맨 끝 숫자는 달라도 됨
"""

import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# 경기 링크의 베이스 URL
base_url = "https://esports.op.gg/valorant/matches/{}/dis-vs-boom"

# 데이터프레임 객체를 담을 빈 리스트를 초기화
dfs = []

def get_league_info(soup):
    try:
        league_info = soup.select_one("#__next > div.__variable_b05285.__variable_1df009.__variable_2de02f.font-roboto > div > main > div.content.w-full.flex-1.transition-all > div.mb-\\[28px\\].mt-3.flex.flex-col > div.relative.mx-4.flex.flex-col.items-center.md\\:mx-0.md\\:flex-row > div.mb-4.flex.items-center.space-x-2.md\\:mb-0.left-\\[50\\%\\].top-0.md\\:absolute.md\\:-translate-x-\\[50\\%\\] > span")
        return league_info.get_text() if league_info else "정보 없음"
    except Exception as e:
        print(f"리그 정보 추출 중 오류 발생: {e}")
        return "정보 없음"

def get_player_stats(tb, team_name):
    player_stats = []
    try:
        # 플레이어 이름, ACS, KDA, ADR, HS%, +/- 통계를 가져옴
        player_names = tb.find_all("a", {'class': 'text-t2 font-bold'})
        acs_stats = tb.find_all("div", {'class': 'text-body1 sm:text-t2 w-full font-bold'})
        kda_stats = tb.find_all("div", {'class': 'text-t2 whitespace-pre font-bold'})
        adr_stats = tb.find_all("td", {'class': 'text-body1 text-center align-top sm:align-middle py-2 lg:w-20 w-14 md:table-cell px-1'})
        hs_stats = tb.find_all("td", {'class': 'text-body1 text-center align-top sm:align-middle py-2 lg:w-20 w-14 md:table-cell pr-2 md:pr-3 px-1'})
        plusminus_stats = tb.find_all("td", {'class': 'text-body1 text-center align-top sm:align-middle py-2 sm:w-[58px] w-10 sm:table-cell hidden lg:table-cell px-1'})
        
        # 각 플레이어가 사용한 에이전트 추출
        player_rows = tb.find_all("tr")
        for i in range(min(5, len(player_rows))):  # 상위 5명의 플레이어로 제한
            player = {}
            player['name'] = player_names[i].text.strip() if i < len(player_names) else ""
            player['team'] = team_name
            player['acs'] = acs_stats[i].text.strip() if i < len(acs_stats) else ""
            player['kda'] = kda_stats[i].text.strip() if i < len(kda_stats) else ""
            player['adr'] = adr_stats[i].text.strip() if i < len(adr_stats) else ""
            player['hs%'] = hs_stats[i].text.strip() if i < len(hs_stats) else ""
            player['+/-'] = plusminus_stats[i].text.strip() if i < len(plusminus_stats) else ""
            
            # 에이전트 추출
            agents = []
            ul = player_rows[i].find("div")
            if ul:
                img_tags = ul.find_all("img")
                for img in img_tags:
                    if 'alt' in img.attrs:
                        if img['alt'] != team_name:
                            agents.append(img['alt'])
                    else:
                        agents.append("")
            player['agents'] = agents
            
            player_stats.append(player)
    
    except IndexError as e:
        print(f"Error extracting player stats: {e}")
    
    return player_stats

def extract_team_data(soup):
    teams = []
    try:
        for i in range(2):  # 두 팀을 순회
            team = {}
            tb = soup.find_all("tbody")[i]
            team_name = tb.find("div", {'class': 'text-body2 text-gray-400'}).text.strip() if tb else ""
            team['players'] = get_player_stats(tb, team_name)
            teams.append(team)
    except IndexError as e:
        print(f"Error extracting team data: {e}")
    
    return teams

def extract_map_urls(soup):
    # 맵 버튼을 찾아 추출
    map_buttons = soup.find_all("ul", {'class': 'mb-1 flex space-x-1'})[0].find_all('button')
    map_urls = [button.text for button in map_buttons]
    return map_urls

def scrape_page(driver, url, map_name, soup):
    global dfs
    df = pd.DataFrame(columns=['league', 'map', '선수명', '팀명', '사용요원', 'ACS', 'KDA', '+/-', 'ADR', 'Hs%', 'WL', '리그정보'])
    
    try:
        league = int(url.split('/')[-2])  # URL에서 리그 번호 추출
    except ValueError:
        print(f"Failed to extract league number: {url}")
        return
    
    teams = extract_team_data(soup)
    wl = [wl.text for wl in soup.find_all("div", {'class': 'm-1 flex items-center justify-center h-5 w-5'})]

    for i, team in enumerate(teams):
        for player in team['players']:
            df.loc[len(df)] = {
                'league': league,
                'map': map_name,
                '선수명': player['name'],
                '팀명': player['team'],
                '사용요원': player['agents'],
                'ACS': player['acs'],
                'KDA': player['kda'],
                '+/-': player['+/-'],
                'ADR': player['adr'],
                'Hs%': player['hs%'],
                'WL': wl[i],
                '리그 정보': get_league_info(soup)
            }

    dfs.append(df)

# Selenium WebDriver 설정
driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH

# 1부터 50까지의 각 경기 번호에 대해 반복
for match_number in range(1, 500):
    # 현재 경기의 URL 구성
    match_url = base_url.format(match_number)
    
    driver.get(match_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    html = driver.page_source
    soup = bs(html, 'lxml')
    map_urls = extract_map_urls(soup)

    for map_name in map_urls:  # 모든 맵 버튼 클릭
        button = driver.find_element(By.XPATH, f"//button[text()='{map_name}']")
        button.click()
        time.sleep(3)  # 클릭 후 페이지 로딩 대기
        html = driver.page_source
        soup = bs(html, 'lxml')
        scrape_page(driver, match_url, map_name, soup)
        
    # 모든 데이터프레임을 하나로 병합
    final_df = pd.concat(dfs, ignore_index=True)
    dfs = []

    # Excel 파일로 저장
    filename = f'val_league_maps_{match_number}.xlsx'
    final_df.to_excel(filename, index=False)

driver.quit()
