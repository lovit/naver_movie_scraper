from bs4 import BeautifulSoup
from glob import glob
import json
import math
import re
import requests
import time


url_base = 'https://movie.naver.com/movie/point/af/list.nhn?st=nickname&target=after&sword={}'

def scrap_comments_of_a_user(seed_idx, sleep=0.1):
    """
    Usage
    -----
        >>> seed_idx = '123467' # comment seed idx
        >>> comments, n_exceptions, flag = scrap_comments_of_a_user(seed_idx)
    """
    url = url_base.format(seed_idx)
    soup, max_page = get_comment_soup(url)

    comments = []
    n_exceptions = 0

    comments_, n_exceptions_ = parse_comments(soup)
    comments += comments_
    n_exceptions += n_exceptions_

    # available only to 1000 page
    max_page = min(max_page, 999)

    if max_page > 1:
        for page in range(2, max_page+1):
            time.sleep(sleep)
            try:
                url_ = f'{url}&page={page}'
                soup, max_page = get_comment_soup(url_)
                comments_, n_exceptions_ = parse_comments(soup)
                comments += comments_
                n_exceptions += n_exceptions_
                print(f'\rscraping with seed = {seed_idx}, page = {page}/{max_page}', end='')
            except:
                return comments, n_exceptions, False
    return comments, n_exceptions, True

normalize_pattern = re.compile('[\r\n\t]')
doublespace_pattern = re.compile('[\s]+')

def normalize_text(text):
    """
    Usage
    -----
        >>> normalize_text('이건 \t\t\t정말\n  짱야  !! ')
        $ '이건 정말 짱야 !!'
    """
    text = normalize_pattern.sub(' ', text)
    text = doublespace_pattern.sub(' ', text)
    return text.strip()

def get_comment_soup(url):
    r = requests.get(url, allow_redirects=True)
    max_page = get_max_page(r)

    b = r.text.index('<!-- list -->')
    e = r.text.index('<!-- //list -->') + 15
    soup = BeautifulSoup(r.text[b:e], 'lxml')
    return soup, max_page

def get_max_page(r):
    e = r.text.index("</strong>개의 평점이 있습니다")
    b = r.text.rindex('>', 0, e) + 1
    count = int(r.text[b:e].replace(',','').replace(' ', '').strip())
    max_page = math.ceil(count/10)
    return max_page

def parse_comments(soup):
    def parse(tr):
        movie_link = tr.select('a[href^="?st=mcode&sword="]')[0].attrs['href']
        b = movie_link.index('sword=')+6
        e = movie_link.index('&', b)
        movie_idx = int(movie_link[b:e])
        idx, _, score, text, timestamp = tr.text.strip().split('\n\n')
        idx = int(idx)
        score = int(score.split()[-1].replace('중', ''))
        text = text.strip()
        # remove "신고"
        text = text[:-2].strip()
        # normalize
        text = normalize_text(text)
        timestamp = timestamp.split('**')[-1].strip()
        return {'idx': idx, 'movie_idx':movie_idx, 'score': score, 'written_at': timestamp, 'text': text}

    trs = soup.select('tr')[1:]
    comments = []
    n_exceptions = 0
    for tr in trs:
        try:
            comments.append(parse(tr))
        except Exception as e:
            n_exceptions += 1
    return comments, n_exceptions

def scan_comment_indices(comments_dir, debug=False):
    """
    Usage
    -----
        >>> indices = scan_comment_indices('./comments/')
    """
    paths = glob(f'{comments_dir}/*')
    if debug:
        paths = paths[:10]
    indices = set()
    n_exceptions = 0
    n_paths = len(paths)
    for i, path in enumerate(paths):
        with open(path, encoding='utf-8') as f:
            for line in f:
                try:
                    indices.add(int(json.loads(line.strip())['idx']))
                except:
                    n_exceptions += 1
                    continue
        if i % 1000 == 0:
            n_indices = len(indices)
            percent = 100 * (i+1) / n_paths
            print(f'\rscanning from {i+1} / {n_paths} ({percent:.4}%): found {n_indices} indices, {n_exceptions} exceptions', end='')

    n_indices = len(indices)
    suffix = ' ' * 20
    print(f'\rscanning has been done. found {n_indices} indices, {n_exceptions} exceptions{suffix}')
    return indices
