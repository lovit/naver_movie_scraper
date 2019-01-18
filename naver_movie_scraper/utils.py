import json
import re
import requests
import sys
from bs4 import BeautifulSoup
from pprint import pprint


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
    """
    Arguments
    ---------
    s : str
        Text to normalize

    Returns
    -------
    normalized text. Remove \\n, \\r, \\t, double space
    """

    s = s.replace('&nbsp;', ' ')
    s = s.replace('\xa0', ' ')
    s = normalize_pattern.sub(' ', s)
    s = doublespcae_pattern.sub(' ', s)
    return s.strip()


def save_list_of_dict(obj, path):
    """
    Arguments
    ---------
    obj : list of dict
        Object to store
    path : str
        File path
    """

    with open(path, 'w', encoding='utf-8') as f:
        for d in obj:
            f.write('{}\n'.format(json.dumps(d, ensure_ascii=False)))

def load_list_of_dict(path):
    """
    Arguments
    ---------
    path : str
        File path

    Returns
    -------
    obj : list of dict
        Object to store
    """

    with open(path, encoding='utf-8') as f:
        objs = [json.loads(obj.strip()) for obj in f]
    return objs

def save_json(obj, path):
    """
    Arguments
    ---------
    obj : list of dict
        Object to store
    path : str
        File path
    """

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)