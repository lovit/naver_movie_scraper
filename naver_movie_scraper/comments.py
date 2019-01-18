import math
import re
import time
from .utils import get_soup


comments_url_form = 'http://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code={}&type={}&onlyActualPointYn=N&order=newest&page={}' # idx, type, page

def scrap_comments(idx, limit=-1, sleep=0.05):
    comments = _scrap_comments(idx, limit, after=True, sleep=sleep)
    comments += _scrap_comments(idx, limit, after=False, sleep=sleep)
    return comments

def _scrap_comments(idx, limit, after, sleep=0.05):
    after_strf = 'after' if after else 'before'
    max_page = num_of_comment_pages(idx, after)
    if limit > 0:
        max_page = min(limit, max_page)
    if max_page <= 0:
        return []

    comments = []
    for p in range(1, max_page + 1):
        url = comments_url_form.format(idx, 'after' if after else 'before', p)
        comments += parse_a_page(get_soup(url))
        if p % 20 == 0:
            print('\r  movie {}, {}, {} / {} ...'.format(idx, after_strf, p, max_page), end='')
    print('\r  movie {}, {}, {} / {} done'.format(idx, after_strf, p, max_page))
    return comments

def parse_a_page(soup):
    comments = []
    for row in soup.select('div[class=score_result] li'):
        try:
            score = int(row.select('div[class=star_score] em')[0].text.strip())
            text = row.select('div[class=score_reple] p')[0].text.strip()
            user = row.select('a[onclick^=javascript]')[0].attrs.get('onclick', '').split('(')[1].split(',')[0]
            written_at = re.search(r"\d+\.\d+\.\d+ \d+:\d+", row.text).group()
            agree = int(row.select('span[class^=sympathy]')[0].text.strip())
            disagree = int(row.select('span[class^=notSympathy]')[0].text)
            comments.append(
                {'score': score,
                 'text': text,
                 'user': user,
                 'written_at': written_at,
                 'agree': agree,
                 'disagree': disagree
                })
        except:
            continue
    return comments

def num_of_comment_pages(idx, after=True):
    url = comments_url_form.format(idx, 'after' if after else 'before', 1)
    soup = get_soup(url)

    try:
        num_comments = int(soup.select('div[class=score_total] em')[1].text.replace(',',''))
        return math.ceil(num_comments / 5)
    except Exception as e:
        return 0
