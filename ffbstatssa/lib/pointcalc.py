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
    strip_crap(soup)
    stat_table1 = soup.find('table', attrs={'id' : 'statTable1'})
    pattern = re.compile('((odd|even) first)|(odd$|even$)')
    rows = stat_table1.findAll('tr', attrs={'class' : pattern})
    stats = []
    for row in rows:
        position = row.find('td', attrs={'class' : 'pos first'}).contents[0]
        player = row.find('td', attrs={'class' : 'player'})
        player = player.contents[0].contents[0].contents[0]
        points = row.find('td', attrs={'class' : 'pts stat last'}).contents[0]
        stats.append([position, player, points])
    for stat in stats:
        print stat