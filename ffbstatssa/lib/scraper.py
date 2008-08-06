import cookielib
import pkg_resources
from urllib import urlencode
from urllib2 import Request, urlopen, URLError

pkg_resources.require("BeautifulSoup>=3.0.0")
from BeautifulSoup import BeautifulSoup


class FantasyFootballPageScraper():
    def __init__(self, username, passwd):
        self.USER_AGENT = ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; '
                      'rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1')
        self.ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        self.ACCEPT_LANGUAGE = 'en-us,en;q=0.5'
        self.ACCEPT_CHARSET = 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
        self.KEEP_ALIVE = '300'
        self.CONNECTION = 'keep-alive'
        self.CONTENT_TYPE = 'application/x-www-form-urlencoded'
        
        self.username = username
        self.passwd = passwd        
        self.cookiejar = cookielib.CookieJar()
        self.soup = None
        
        postdata = self._get_postdata()
        self._login(postdata)
    
    def _display_url_error(self, e):
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfil the request.'
            print 'Error code', e.code
        
    def _get_postdata(self):
        url = 'https://login.yahoo.com/'
        headers = {
            'Host' : 'login.yahoo.com',
            'User-Agent' : self.USER_AGENT,
            'Accept' : self.ACCEPT,
            'Accept-Language' : self.ACCEPT_LANGUAGE,
            'Accept-Charset' : self.ACCEPT_CHARSET,
            'Keep-Alive' : self.KEEP_ALIVE,
            'Connection' : self.CONNECTION
        }
        request = Request(url, headers=headers)
        try:
            response = urlopen(request)
        except URLError, e:
            self._display_url_error(e)
        else:
            self.cookiejar.extract_cookies(response, request)
            doc = response.readlines()
            soup = BeautifulSoup(''.join(doc))
            hidden_inputs = soup.findAll('input', attrs={'type' : 'hidden'})
            data = {}
            for input in hidden_inputs:
                data[input.attrMap['name']] = str(input.attrMap['value'])
            data['login'] = self.username
            data['passwd'] = self.passwd
            return urlencode(data)
        
    def _login(self, data):
        url = 'https://login.yahoo.com/config/login'
        headers = {
            'Host' : 'login.yahoo.com',
            'Referer' : 'https://login.yahoo.com/',
            'User-Agent' : self.USER_AGENT,
            'Accept' : self.ACCEPT,
            'Accept-Language' : self.ACCEPT_LANGUAGE,
            'Accept-Charset' : self.ACCEPT_CHARSET,
            'Keep-Alive' : self.KEEP_ALIVE,
            'Connection' : self.CONNECTION,
            'Content-Type' : self.CONTENT_TYPE,
            'Content-Length' : len(data)
        }

        request = Request(url, data, headers)
        self.cookiejar.add_cookie_header(request)
        request.headers['Cookie'] = request.unredirected_hdrs['Cookie']
        
        try:
            response = urlopen(request)
        except URLError, e:
            self._display_url_error(e)
        else:
            self.cookiejar.extract_cookies(response, request)
    
    def get_ffb_page(self, page='/f2/5973'):
        url = ''.join(['http://football.fantasysports.yahoo.com', page])
        headers = {
            'Host' : 'football.fantasysports.yahoo.com',
            'User-Agent' : self.USER_AGENT,
            'Accept' : self.ACCEPT,
            'Accept-Language' : self.ACCEPT_LANGUAGE,
            'Accept-Charset' : self.ACCEPT_CHARSET,
            'Keep-Alive' : self.KEEP_ALIVE,
            'Connection' : self.CONNECTION
        }
        
        request = Request(url, headers=headers)
        self.cookiejar.add_cookie_header(request)
        request.headers['Cookie'] = request.unredirected_hdrs['Cookie']
        try:
            response = urlopen(request)
        except URLError, e:
            self._display_url_error(e)
        else:
            doc = response.readlines()
            self.soup = BeautifulSoup(''.join(doc))

if __name__ == '__main__':
    scraper = FantasyFootballPageScraper()
    print scraper.soup.prettify()