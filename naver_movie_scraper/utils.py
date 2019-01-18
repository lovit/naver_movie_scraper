import sys
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re


normalize_pattern = re.compile('[\r\n\t]')
doublespcae_pattern = re.compile('[\s]+')


def get_soup(url):
    """
    Argument
    --------
    url : str
        Web page url

    Returns
    -------
    bs4.Beautifulsoup format HTML page
    """

    try:
        r = requests.get(url).text
        return BeautifulSoup(r, 'lxml')
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = {
            'filename': exc_traceback.tb_frame.f_code.co_filename,
            'lineno'  : exc_traceback.tb_lineno,
            'name'    : exc_traceback.tb_frame.f_code.co_name,
            'type'    : exc_type.__name__,
            'message' : str(e)
        }
        pprint(traceback_details)
        return ''

def text_normalize(s):
    s = normalize_pattern.sub(' ', s)
    s = doublespcae_pattern.sub(' ', s)
    return s.strip()
