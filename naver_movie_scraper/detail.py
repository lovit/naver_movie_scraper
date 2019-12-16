from .utils import get_soup


detail_url_form = 'http://movie.naver.com/movie/bi/mi/detail.nhn?code={}' # idx

def scrap_casting(idx):
    url = detail_url_form.format(idx)
    soup = get_soup(url)

    directors = [parse_director(div) for div in soup.select('div[class=dir_product]')]
    directors = [d for d in directors]
    actors = [parse_actor(actor, i+1) for i, actor in enumerate(soup.select('div[class=p_info]'))]
    actors = [actor for actor in actors if actor]
    staffs = [parse_staff(staff) for staff in soup.select('table[class=staff_lst] span')]
    staffs = [staff for staff in staffs if staff]

    return {
        'directors': directors,
        'actors': actors,
        'staffs': staffs
    }

def parse_director(director):
    try:
        director_id = director.select('a')
        if director_id:
            director_id = int(director_id[0].attrs.get('href','=').split('=')[1])
        k_name = director.select('a[class=k_name]')
        k_name = k_name[0].text.strip() if k_name else ''
        e_name = director.select('em[class=e_name]')
        e_name = e_name[0].text.strip() if e_name else ''
        return {'id': director_id, 'k_name': k_name, 'e_name': e_name}
    except Exception as e:
        return {}

def parse_actor(actor, i):
    try:
        actor_id = actor.select('a')
        if actor_id:
            actor_id = int(actor_id[0].attrs.get('href','=').split('=')[1])
        k_name = actor.select('a[class=k_name]')
        k_name = k_name[0].text.strip() if k_name else ''
        e_name = actor.select('em[class=e_name]')
        e_name = e_name[0].text.strip() if e_name else ''
        part = actor.select('em[class=p_part]')
        part = part[0].text.strip() if part else ''
        role = actor.select('p[class=pe_cmt]')
        role = role[0].text.replace('[\n역]','').strip() if role else ''
        return {'id': actor_id, 'k_name': k_name, 'e_name': e_name, 'part': part, 'role': role, 'casting_order': i}
    except:
        return {}

def parse_staff(staff):
    try:
        idx = int(staff.select('a')[0].attrs.get('href', '=').split('=')[1])
        k_name = staff.select('a')[0].text
        e_name = ''
        role = ''
        for em in staff.select('em'):
            em = em.text
            if '(' in em: role = em.replace('(', '').replace(')','')
            else: e_name = em
        return {'id': idx, 'k_name': k_name, 'e_name': e_name, 'role': role}
    except:
        return {}