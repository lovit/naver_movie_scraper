import re
from bs4 import BeautifulSoup
from .utils import get_soup
from .utils import text_normalize


basic_url_form = 'http://movie.naver.com/movie/bi/mi/basic.nhn?code={}' # idx

def scrap_basic(idx):
    url = basic_url_form.format(idx)
    soup = get_soup(url)
    infomation = {
        'movie_idx': idx,
        'expert_score': meta_score(soup)[0],
        'netizen_score': meta_score(soup)[1],
        'title': title(soup),
        'e_title': e_title(soup),
        'genres': genres(soup),
        'countries': countries(soup),
        'running_time': running_time(soup),
        'open_date': open_date(soup),
        'grade': grade(soup),
        'story': story(soup),
        'making_note': making_note(soup),
        'box_office': box_office(soup)
    }
    return infomation

def meta_score(soup):
    try:
        main_score = soup.select('div[class=main_score]')[0]
        expert_score = main_score.select('div[class=spc_score_area] div[class=star_score]')[0].text.replace('\n','')
        netizen_score = main_score.select('div[class=star_score] span[class=st_off]')[0].text.replace('관람객 평점 ', '').replace('점', '')
        return float(expert_score), float(netizen_score)
    except:
        return -1, -1

def title(soup):
    a = soup.select('div[class=mv_info] h3[class=h_movie] a')
    if not a:
        return ''
    return text_normalize(a[0].text)

def e_title(soup):
    strong = soup.select('div[class=mv_info] strong[class=h_movie2]')
    if not strong:
        return ''
    return text_normalize(strong[0].text)

def genres(soup):
    genres = soup.select('a[href^=/movie/sdb/browsing/bmovie.nhn?genre=]')
    return list({genre.text for genre in genres})
    
def countries(soup):
    countries = soup.select('a[href^=/movie/sdb/browsing/bmovie.nhn?nation=]')
    return list({country.text for country in countries})

def running_time(soup):
    dl = soup.select('dl[class=info_spec]')
    try:
        return int(re.search(r"\d+분", dl[0].text).group()[:-1])
    except:
        return 0

def open_date(soup):
    links = soup.select('dl[class=info_spec] a')
    dates = [a.attrs['href'].split('bmovie.nhn?open=')[-1]
        for a in links if 'bmovie.nhn?open=' in a.attrs.get('href', '')]
    dates = ['{}-{}-{}'.format(d[:4], d[4:6], d[6:]) for d in dates if len(d) == 8]
    return dates
    
def grade(soup):
    a = soup.select('a[href^=/movie/sdb/browsing/bmovie.nhn?grade]')
    if not a:
        return ''
    return text_normalize(a[0].text)

def story(soup):
    try:
        story_soup = BeautifulSoup(
            str(soup.select("div[class=story_area]")[0]).replace('<br>', '\n').replace('\xa0', '\n'),
            'lxml')
        sents = story_soup.text.split('\n')
        sents = [text_normalize(s) for s in sents if s]
        sents = [s for s in sents if s != '줄거리']
        return '\n'.join(sents)
    except:
        return ''

def making_note(soup):
    try:
        note_soup = BeautifulSoup(
            str(soup.select('div[class=making_note]')[0]).replace('<br>', '\n').replace('\xa0', '\n'),
            'lxml')
        sents = note_soup.text.split('\n')
        sents = [text_normalize(s) for s in sents if s]
        sents = [s for s in sents if not s == '펼쳐보기']
        return '\n'.join(sents)
    except:
        return ''

def box_office(soup):
    p = soup.select('p[class=count]')
    if not p:
        return -1
    return text_normalize(p[0].text)