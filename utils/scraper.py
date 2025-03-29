import requests, re, os, urllib.request, ssl, time
from unidecode import unidecode
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

class Scraper:
    def __init__(self):
        self.user_agent = os.getenv('USER_AGENT')
        self.visited = {}

    def scrape(self, url, min_load=100, names=False):
        url = self.clean_url(url)

        if not url:
            return ''
        
        text = self.requests_scrape(url, text_format=True)

        # If javascript is required, scrape with selenium

        if re.search('enable javascript', ''.join([s.lower() for s in text])) or len(''.join(text)) < min_load:
            print('Using selenium on', url)
            text = self.selenium_scrape(url, text_format=True)

        self.visited[url] = text

        return [i for i in self.remove_junk(text, names) if i]

    def requests_scrape(self, url, text_format=False, retries=3):
        while retries > 0:
            try:
                headers = {'User-Agent': self.user_agent}
                response = requests.get(url, headers=headers, timeout=30)
                soup = BeautifulSoup(response.text, 'html.parser')

                if not text_format:
                    return soup
                
                text = soup.get_text('\n').split('\n')
                return text
            except:
                time.sleep(5)
                retries -= 1
        return []

    def selenium_scrape(self, url, text_format=False, retries=3):
        while retries > 0:
            try:
                driver = self.selenium_web_driver_setup()
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                driver.quit()

                if not text_format:
                    return soup
                
                text = soup.get_text('\n').split('\n')
                return text
            except:
                time.sleep(5)
                retries -= 1
        return []

    def selenium_web_driver_setup(self):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"--user-agent={self.user_agent}")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('log-level=3')

        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        os.chmod(f'{os.path.dirname(os.path.realpath(__file__))}/Chrome/chromedriver.exe', 755)
        return webdriver.Chrome(
            service = ChromeService(executable_path=f'{os.path.dirname(os.path.realpath(__file__))}/Chrome/chromedriver.exe'), 
            options = chrome_options
        )
    
    def clean_url(self, url):

        # Check if url is valid

        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            print('invalid url scheme:', url)
            return ''

        # Blacklist irrelevant pages
        
        blacklist = [
            'store-locator',
            'share',
            'faq',
            'terms-of-service',
            'terms-of-use',
            'termsofuse',
            'settings',
            'contact',
            'careers',
            'register',
            'sign-up',
            'login',
            'signup',
            'termsofservice',
            '/search?',
            'accounts',
            'users',
            '/cart',
            '/checkout',
            '/privacy$',
            '/find-apps',
            '.pdf',
            'legal-notice',
            'get-started',
            'getstarted',
            '/legal',
            'sign_in',
            'signin',
            'personal-information',
            'personalinformation',
            'legal-information',
            'privacy-policy',
            'publications',
            'media',
            'support',
            '/trial',
            'freetrial',
            'free-trial',
            '/account$',
            '/download',
            '/security/',
            '/cookie-policy',
            'terms-conditions'
        ]
        if len(url.split('//')[1].split('/')) > 1:
            if re.search(r'|'.join(blacklist), '/' + '/'.join(url.split('//')[1].split('/')[1:])):
                return ''

        # Blacklist other languages
           
        languages = ['uk', 'km', 'tr', 'es', 'lv', 'az', 'mg', 'ky', 'ml', 'ms', 'jv', 'sn', 'mn', 'hu', 'om', 'ro', 'yo', 'de', 'da', 'su', 'hi', 'cy', 'he', 'sk', 'ku', 'lt', 'ne', 'mk', 'nl', 'fr', 'pa', 'af', 'bg', 'ja', 'kn', 'kk', 'sr', 'hy', 'te', 'ru', 'zh', 'ha', 'vi', 'eu', 'xh', 'pl', 'sd', 'th', 'ff', 'nb', 'ta', 'sw', 'it', 'ceb', 'ma', 'mr', 'as', 'gu', 'bn', 'ur', 'ar', 'ca', 'uz', 'fi', 'el', 'my', 'sq', 'cs', 'zu', 'sl', 'gl', 'sv', 'wo', 'hr', 'so', 'et', 'id', 'ko', 'ka', 'ig', 'si', 'pt', 'tl', 'fa']
        
        if len(url.split('//')[1].split('/')) > 1:
            language_filter = r'/(' + r'|'.join(languages) + r')($|-|_)'
            if re.search(language_filter, '/' + '/'.join(url.split('//')[1].split('/')[1:])):
                return ''

        url = url.split('#')[0]
        
        return url
        
    def remove_junk(self, text, names):
        blacklist = [
            'copyright',
            'last updated',
            'please contact',
            'contact us',
            'terms and conditions',
            'terms & conditions',
            'home page',
            'homepage',
            'about us',
            'login',
            'recaptcha',
            'privacy policy',
            'terms of service',
            'get in touch',
            'join now',
            'agree & join',
            'agree and join',
            'microsoft store',
            'log in',
            'sign up',
            'all rights reserved',
            'cookies enabled',
            'submit or claim',
            'create an account',
            'please enter',
            'by continuing, you agree',
            'free sign-up',
            'please confirm',
            'clicking here',
            'click here',
            'free account',
            'something went wrong',
            'please try again',
            'enable javascript',
            'click the link',
            'you agree to',
            'stay up to date',
            'your submission',
            'you can find their website',
            'password',
            'save to custom',
            'get notified',
            'for more details',
            'set up your account',
            'to complete this action',
            'this website uses cookies',
            'download the app',
            '©',
            'you\'ve scrolled',
        ]
        result = []
        for s in text:
            if len(s) == 0:
                continue
            flag = True
            if re.search(r'|'.join(blacklist), s.lower()):
                flag = False

            # If sentence does not:
            #   contain any blacklisted words
            #   has more than 4 words
            #   is not html
            # Add it but remove punctuation
            if flag and (len(s.split()) > 4 or names) and (s[0] != '<' and s[-1] != '>'):
                s = ' '.join(s.split())
                if len(s) == 0:
                    continue
                if s[-1] in '.?,!':
                    s = s[:-1]
                if s:
                    result.append(unidecode(s))
        if result and result[-1] and result[-1][-1] != '.':
            result.append('')
        return result
    
