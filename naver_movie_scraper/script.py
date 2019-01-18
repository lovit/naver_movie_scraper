import math
import time
from .utils import get_soup
from .utils import text_normalize


script_url_form = 'http://movie.naver.com/movie/bi/mi/script.nhn?code={}&page={}' # idx, page

def scrap_bestscripts(idx, limit=-1, sleep=0.05):
    scripts = []
    max_page = num_of_bestscript_pages(idx)
    for p in range(1, max_page + 1):
        url = script_url_form.format(idx, p)
        soup = get_soup(url)
        scripts += scrap_from_a_page(soup)
        time.sleep(sleep)
        if limit > 0 and limit <= p:
            break
    return scripts

def scrap_from_a_page(soup):
    scripts = []
    for script in soup.select('ul[class=lines] li div[class=lines_area2]'):
        try:
            text = text_normalize(script.select('p[class=one_line]')[0].text)
            character = text_normalize(script.select('p[class=char_part]')[0].text)
            description = text_normalize(script.select('p[class=line_desc]')[0].text)
            agree = int(script.select('span[class=w_recomm] em')[-1].text)
            scripts.append(
                {'text': text,
                 'chracter': character,
                 'description': description,
                 'num_agree': agree
                })
        except Exception as e:
            continue
    return scripts

def num_of_bestscript_pages(idx):
    url = script_url_form.format(idx, 1)
    soup = get_soup(url)

    try:
        num_scripts = int(soup.select('span[class=cnt] em')[0].text.replace(',',''))
        return math.ceil(num_scripts / 10)
    except Exception as e:
        return 0