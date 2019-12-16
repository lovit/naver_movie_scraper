import math
import re
import time
from .utils import get_soup


comments_url_form = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code={}&order=newest&page={}&onlySpoilerPointYn=N' # idx, type, page

def scrap_comments(idx, limit=-1, sleep=0.05, last_time=None):
    max_page = num_of_comment_pages(idx)
    if limit > 0:
        max_page = min(limit, max_page)
    if max_page <= 0:
        return []

    comments = []
    for p in range(1, max_page + 1):
        url = comments_url_form.format(idx, p)
        comments_p, stop = parse_a_page(get_soup(url), last_time)
        if p % 20 == 0:
            print(f'\r  movie {idx}, {p} / {max_page} ...', end='')
        comments += comments_p
        if stop:
            print(f'\r  movie {idx}. stop scrap comments. found existing comments {p} / {max_page}')
            break
    if not stop:
        print(f'\r  movie {idx}, {p} / {max_page} done')
    return comments[::-1]

def parse_a_page(soup, last_time=None):
    comments = []
    stop = False
    for row in soup.select('div[class=score_result] li'):
        try:
            score = int(row.select('div[class=star_score] em')[0].text.strip())
            text = row.select('div[class=score_reple] p')[0].text.strip()
            # detach '관람객' icon
            if text[:4] == '관람객\n':
                text = text[4:].strip()
            # detach '스포일러' icon
            if text[:25] == '스포일러가 포함된 감상평입니다. 감상평 보기\n':
                text = text[25:].strip()
            idx = row.select('a[onclick^=javascript]')[0].attrs.get('onclick', '').split('(')[1].split(',')[0]
            masked_user = row.select('div[class=score_reple] em')[0].text.strip()
            written_at = re.search(r"\d+\.\d+\.\d+ \d+:\d+", row.text).group()
            agree = int(row.select('strong[class^="sympathy"]')[0].text.strip())
            disagree = int(row.select('strong[class^="notSympathy"]')[0].text.strip())
            if (last_time is not None) and (written_at <= last_time):
                stop = True
                break
            comments.append(
                {'score': score,
                 'text': text,
                 'idx': idx,
                 'user': masked_user,
                 'written_at': written_at,
                 'agree': agree,
                 'disagree': disagree
                })
        except Exception as e:
            continue
    return comments, stop

def num_of_comment_pages(idx):
    url = comments_url_form.format(idx, 1)
    soup = get_soup(url)

    try:
        num_comments = int(soup.select('div[class="score_total"] em')[-1].text.replace(',',''))
        return math.ceil(num_comments / 5)
    except Exception as e:
        return -1
