import re
from scraper import FantasyFootballPageScraper
import config_scraper as cfg

ffb = FantasyFootballPageScraper(cfg.username, cfg.password, cfg.league_path)     
soup = ffb.get_ffb_page('/matchup?week=1&mid1=2&mid2=1')

def strip_crap(soup):
    scripts = soup.findAll('script')
    styles = soup.findAll('style')
    for script in scripts:
        script.extract()
    for style in styles:
        style.extract()

if __name__ == '__main__':
    pattern1 = re.compile('last')
    pattern2 = re.compile('pts')
    strip_crap(soup)
    stat_table1 = soup.find('table', attrs={'id' : 'statTable1'})
    total_row = stat_table1.find('tr', attrs={'class' : pattern1})
    total_pts = total_row.find('td', attrs={'class' : pattern2}).contents[0]
    print total_pts