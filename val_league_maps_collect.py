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

# 크롤링할 매치 URL 리스트
links = [
    "https://esports.op.gg/valorant/matches/10020/lc-vs-cnl-2024-06-12",
    "https://esports.op.gg/valorant/matches/10154/rec-vs-tyr-2024-06-12",
    "https://esports.op.gg/valorant/matches/10018/dis-vs-boom-2024-06-12",
    "https://esports.op.gg/valorant/matches/10021/ns-vs-nongshim%20redforce-2024-06-12",
    "https://esports.op.gg/valorant/matches/9450/nth-vs-fl-2024-06-12",
    "https://esports.op.gg/valorant/matches/10027/btr-vs-arf-2024-06-12",
    "https://esports.op.gg/valorant/matches/10155/osc-vs-aw-2024-06-12",
    "https://esports.op.gg/valorant/matches/9451/sg-vs-rc-2024-06-12",
    "https://esports.op.gg/valorant/matches/10125/medal-vs-vlt-2024-06-12",
    "https://esports.op.gg/valorant/matches/10023/iam-vs-iam-2024-06-12",
    "https://esports.op.gg/valorant/matches/10306/lazy-vs-tear-2024-06-12",
    "https://esports.op.gg/valorant/matches/10153/ns-vs-zol-2024-06-12",
    "https://esports.op.gg/valorant/matches/9977/mith-vs-bnc-2024-06-12",
    "https://esports.op.gg/valorant/matches/9955/da%20feng%20gou-vs-of-2024-06-12",
    "https://esports.op.gg/valorant/matches/9950/papa%20esports-vs-fa-2024-06-12",
    "https://esports.op.gg/valorant/matches/10064/nig-vs-rda-2024-06-12",
    "https://esports.op.gg/valorant/matches/9956/roa-vs-hkuf-2024-06-12",
    "https://esports.op.gg/valorant/matches/10115/tr-vs-rge-2024-06-12",
    "https://esports.op.gg/valorant/matches/9978/xia-vs-xerxia-2024-06-12",
    "https://esports.op.gg/valorant/matches/10305/fcy-vs-lofi-2024-06-12",
    "https://esports.op.gg/valorant/matches/10060/ele-vs-dsg-2024-06-12",
    "https://esports.op.gg/valorant/matches/9957/team%20kobolds-vs-one-2024-06-12",
    "https://esports.op.gg/valorant/matches/9564/gl-vs-iwc-2024-06-12",
    "https://esports.op.gg/valorant/matches/9359/gne-vs-nom-2024-06-13",
    "https://esports.op.gg/valorant/matches/9782/ug-vs-drgn-2024-06-13",
    "https://esports.op.gg/valorant/matches/9779/ue-vs-ult-2024-06-13",
    "https://esports.op.gg/valorant/matches/9487/fks-vs-ova-2024-06-13",
    "https://esports.op.gg/valorant/matches/9361/z10-vs-ace%20-2024-06-13",
    "https://esports.op.gg/valorant/matches/9571/gs-vs-s2g-2024-06-13",
    "https://esports.op.gg/valorant/matches/9482/nxt-vs-pu-2024-06-13",
    "https://esports.op.gg/valorant/matches/9762/ig-vs-gtz-2024-06-13",
    "https://esports.op.gg/valorant/matches/9763/fuzos-vs-saw-2024-06-13",
    "https://esports.op.gg/valorant/matches/10098/yfp-vs-tt-2024-06-13",
    "https://esports.op.gg/valorant/matches/9914/hb-vs-sg-2024-06-13",
    "https://esports.op.gg/valorant/matches/9764/ftw-vs-ex0-2024-06-13",
    "https://esports.op.gg/valorant/matches/9765/hof-vs-ppp-2024-06-13",
    "https://esports.op.gg/valorant/matches/9913/2game-vs-2game%20esports-2024-06-13",
    "https://esports.op.gg/valorant/matches/10099/bln-vs-sad-2024-06-13",
    "https://esports.op.gg/valorant/matches/10026/lc-vs-arf-2024-06-13",
    "https://esports.op.gg/valorant/matches/10151/ju-vs-sub-2024-06-13",
    "https://esports.op.gg/valorant/matches/10035/superfect%20esports-vs-spg-2024-06-13",
    "https://esports.op.gg/valorant/matches/10028/thd-vs-dis-2024-06-13",
    "https://esports.op.gg/valorant/matches/9448/sz-vs-scarz-2024-06-13",
    "https://esports.op.gg/valorant/matches/10152/cmm-vs-aw-2024-06-13",
    "https://esports.op.gg/valorant/matches/10025/cnl-vs-ae-2024-06-13",
    "https://esports.op.gg/valorant/matches/10032/dk-vs-slt-2024-06-13",
    "https://esports.op.gg/valorant/matches/9449/sg-vs-fl-2024-06-13",
    "https://esports.op.gg/valorant/matches/10307/unicorn%20cyber-vs-tf-2024-06-13",
    "https://esports.op.gg/valorant/matches/9960/da%20feng%20gou-vs-hkuf-2024-06-13",
    "https://esports.op.gg/valorant/matches/9982/fs-vs-nkt-2024-06-13",
    "https://esports.op.gg/valorant/matches/9958/roa-vs-one-2024-06-13",
    "https://esports.op.gg/valorant/matches/9959/team%20kobolds-vs-fa-2024-06-13",
    "https://esports.op.gg/valorant/matches/10063/nexga-vs-pdf-2024-06-13",
    "https://esports.op.gg/valorant/matches/10156/osc-vs-tyr-2024-06-13",
    "https://esports.op.gg/valorant/matches/10308/bbm-vs-team%20big%20baam-2024-06-13",
    "https://esports.op.gg/valorant/matches/9961/papa%20esports-vs-of-2024-06-13",
    "https://esports.op.gg/valorant/matches/10059/lz-vs-dsg-2024-06-13",
    "https://esports.op.gg/valorant/matches/9983/xoxo-01-vs-spe-2024-06-13",
    "https://esports.op.gg/valorant/matches/9486/cgn-vs-attax-2024-06-14",
    "https://esports.op.gg/valorant/matches/9324/requiem-vs-nxt-2024-06-14",
    "https://esports.op.gg/valorant/matches/9800/tm-vs-ug-2024-06-14",
    "https://esports.op.gg/valorant/matches/9488/sk-vs-sge-2024-06-14",
    "https://esports.op.gg/valorant/matches/9915/hb-vs-tbk-2024-06-14",
    "https://esports.op.gg/valorant/matches/9916/gls-vs-galorys-2024-06-14",
    "https://esports.op.gg/valorant/matches/10100/ffa-vs-tsm-2024-06-14",
    "https://esports.op.gg/valorant/matches/10105/msr-vs-wu-2024-06-14",
    "https://esports.op.gg/valorant/matches/9919/sg-vs-xld-2024-06-14",
    "https://esports.op.gg/valorant/matches/10033/fearx-vs-fearx-2024-06-14",
    "https://esports.op.gg/valorant/matches/10157/osc-vs-sub-2024-06-14",
    "https://esports.op.gg/valorant/matches/10034/iam-vs-spg-2024-06-14",
    "https://esports.op.gg/valorant/matches/9428/nth-vs-rc-2024-06-14",
    "https://esports.op.gg/valorant/matches/10024/btr-vs-boom-2024-06-14",
    "https://esports.op.gg/valorant/matches/10315/edge-vs-kt-2024-06-14",
    "https://esports.op.gg/valorant/matches/10313/rnp-vs-tts-2024-06-14",
    "https://esports.op.gg/valorant/matches/10314/jft-vs-p&l-2024-06-14",
    "https://esports.op.gg/valorant/matches/10037/ns-vs-slt-2024-06-14",
    #"https://esports.op.gg/valorant/matches/10036/dk-vs-dplus-2024-06-14"
    "https://esports.op.gg/valorant/matches/9427/mrg-vs-murash-2024-06-14",
    "https://esports.op.gg/valorant/matches/10158/ju-vs-oas-2024-06-14",
    "https://esports.op.gg/valorant/matches/10029/ae-vs-thd-2024-06-14",
    "https://esports.op.gg/valorant/matches/10334/cyberking%20esports-vs-tf-2024-06-14",
    "https://esports.op.gg/valorant/matches/9985/mith-vs-xia-2024-06-14",
    "https://esports.op.gg/valorant/matches/10061/ele-vs-nig-2024-06-14",
    "https://esports.op.gg/valorant/matches/10335/lazy-vs-fcy-2024-06-14",
    "https://esports.op.gg/valorant/matches/9986/bnc-vs-barn%20nong%20chok-2024-06-14",
    "https://esports.op.gg/valorant/matches/10066/ke-vs-rda-2024-06-14",
    "https://esports.op.gg/valorant/matches/9490/pu-vs-div-2024-06-15",
    "https://esports.op.gg/valorant/matches/9323/sns-vs-apeks-2024-06-15",
    "https://esports.op.gg/valorant/matches/9783/drgn-vs-tm-2024-06-15",
    "https://esports.op.gg/valorant/matches/9491/mouz-vs-nxt-2024-06-15",
    "https://esports.op.gg/valorant/matches/10103/qor-vs-m80-2024-06-15",
    "https://esports.op.gg/valorant/matches/9917/red-vs-2game-2024-06-15",
    "https://esports.op.gg/valorant/matches/10102/oxg-vs-tg-2024-06-15",
    "https://esports.op.gg/valorant/matches/9918/sagaz-vs-lgc-2024-06-15",
    "https://esports.op.gg/valorant/matches/9318/aoi-vs-of-2024-06-15",
    "https://esports.op.gg/valorant/matches/9493/ova-vs-cgn-2024-06-16",
    "https://esports.op.gg/valorant/matches/9654/hge-vs-novo-2024-06-16",
    "https://esports.op.gg/valorant/matches/9418/cas-vs-sol-2024-06-16",
    "https://esports.op.gg/valorant/matches/9655/axl-vs-300-2024-06-16",
    "https://esports.op.gg/valorant/matches/9492/attax-vs-sk-2024-06-16",
    "https://esports.op.gg/valorant/matches/9312/fg-vs-mtz-2024-06-16",
    "https://esports.op.gg/valorant/matches/9656/loneteam-vs-ds-2024-06-16",
    "https://esports.op.gg/valorant/matches/9420/dvm%20esport-vs-jl-2024-06-16",
    "https://esports.op.gg/valorant/matches/9657/op-vs-rtzn-2024-06-16",
    "https://esports.op.gg/valorant/matches/9494/sge-vs-pu-2024-06-16",
    "https://esports.op.gg/valorant/matches/9766/ex0-vs-ig-2024-06-16",
    "https://esports.op.gg/valorant/matches/9496/div-vs-mouz-2024-06-16",
    "https://esports.op.gg/valorant/matches/9767/ppp-vs-ftw-2024-06-17",
    "https://esports.op.gg/valorant/matches/9419/vlnt-vs-akr-2024-06-17",
    "https://esports.op.gg/valorant/matches/9661/ds-vs-300-2024-06-17",
    "https://esports.op.gg/valorant/matches/9680/zeta-vs-zeta%20gaming-2024-06-17",
    "https://esports.op.gg/valorant/matches/9771/hof-vs-fuzos-2024-06-17",
    "https://esports.op.gg/valorant/matches/9659/op-vs-axl-2024-06-17",
    "https://esports.op.gg/valorant/matches/9679/falke%20esports-vs-kpi-2024-06-17",
    "https://esports.op.gg/valorant/matches/9768/gtz-vs-saw-2024-06-17",
    "https://esports.op.gg/valorant/matches/9678/ucam-vs-five-2024-06-17",
    "https://esports.op.gg/valorant/matches/9660/rtzn-vs-hge-2024-06-17",
    "https://esports.op.gg/valorant/matches/9495/nxt-vs-fks-2024-06-17",
    "https://esports.op.gg/valorant/matches/9658/novo-vs-novo%20esports-2024-06-17",
    "https://esports.op.gg/valorant/matches/9675/rbt-vs-bar-2024-06-17",
    "https://esports.op.gg/valorant/matches/9421/zer-vs-mdr-2024-06-17",
    "https://esports.op.gg/valorant/matches/9673/five-vs-zeta-2024-06-18",
    "https://esports.op.gg/valorant/matches/9674/kpi-vs-rbt-2024-06-18",
    "https://esports.op.gg/valorant/matches/9672/imperium%20gaming-vs-imperium%20gaming-2024-06-18",
    "https://esports.op.gg/valorant/matches/9769/ftw-vs-hof-2024-06-18",
    "https://esports.op.gg/valorant/matches/9676/bar-vs-ucam-2024-06-18",
    "https://esports.op.gg/valorant/matches/9770/saw-vs-ex0-2024-06-18",
    "https://esports.op.gg/valorant/matches/9772/ig-vs-ppp-2024-06-18",
    "https://esports.op.gg/valorant/matches/9774/fuzos-vs-gtz-2024-06-18"
]

# 데이터프레임 객체를 담을 빈 리스트를 초기화
dfs = []

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
    df = pd.DataFrame(columns=['league', 'map', '선수명', '팀명', '사용요원', 'ACS', 'KDA', '+/-', 'ADR', 'Hs%', 'WL'])
    
    try:
        league = int(url.split('/')[-2])  # URL에서 리그 번호 추출
    except ValueError:
        print(f"Failed to extract league number: {url}")
        return
    
    teams = extract_team_data(soup)
    wl = [wl.text for wl in soup.find_all("div", {'class': 'm-1 flex items-center justify-center h-9 w-9'})]

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
                'WL': wl[i]
            }

    dfs.append(df)

# Selenium WebDriver 설정
driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH

# 각 매치 링크를 크롤링하는 메인 루프
for link in links:
    driver.get(link)
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
        scrape_page(driver, link, map_name, soup)

driver.quit()

# 모든 데이터프레임을 하나로 병합
final_df = pd.concat(dfs, ignore_index=True)

# 데이터프레임 출력 및 Excel 파일로 저장
print(final_df.head())
final_df.to_excel('val_league_maps.xlsx', index=False)