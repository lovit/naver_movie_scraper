import argparse
import json
import os
import time

from naver_movie_scraper import scrap_basic
from naver_movie_scraper import scrap_casting
from naver_movie_scraper import scrap_bestscripts
from naver_movie_scraper import scrap_comments
from naver_movie_scraper import save_list_of_dict
from naver_movie_scraper import save_json
from naver_movie_scraper import load_list_of_dict


def scrap(idx, directory, casting=True, bestscripts=True, comments=True, limit=3, sleep=0.05, fast_update=False):
    # basic
    path = f'{directory}/meta/{idx}.json'
    if (fast_update) and (os.path.exists(path)):
        print(f'already scraped {idx} basic')
    else:
        save_json(scrap_basic(idx), path)
        print(f'scraped {idx} basic')

    # castings
    if casting:
        path = f'{directory}/actors/{idx}'
        if (fast_update) and (os.path.exists(path)):
            print(f'already scraped {idx} casting')
        else:
            castings = scrap_casting(idx)
            for key in ['actors', 'directors', 'staffs']:
                path = f'{directory}/{key}/{idx}'
                if castings.get(key, []):
                    save_list_of_dict(castings[key], path)
            print(f'scraped {idx} casting')

    # best scripts
    if bestscripts:
        path = f'{directory}/bestscripts/{idx}'
        if (fast_update) and (os.path.exists(path)):
            print(f'already scraped {idx} bests cripts')
        else:
            scripts = scrap_bestscripts(idx, limit, sleep)
            if scripts:
                save_list_of_dict(scripts, path)
            print(f'scraped {idx} best scripts')

    # comments
    if comments:
        path = f'{directory}/comments/{idx}'
        last_time = None
        comments_ = []
        if fast_update:
            if os.path.exists(path):
                comments_ = load_list_of_dict(path)
                last_time = comments_[0]['written_at']
        comments_new = scrap_comments(idx, limit, sleep, last_time)
        if comments_new:
            comments_ += comments_new
            comments_ = {json.dumps(obj, ensure_ascii=False) for obj in comments_}
            comments_ = [json.loads(obj) for obj in comments_]
            comments_ = sorted(comments_, key=lambda x:x['written_at'], reverse=True)
            save_list_of_dict(comments_, path)
        print(f'scraped {len(comments_)} comments of movie {idx}')

    print('')
    time.sleep(sleep)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, default='./output/', help='Output directory')
    parser.add_argument('--begin_idx', type=int, default=134963, help='Index of first movie')
    parser.add_argument('--end_idx', type=int, default=134963, help='Index of last movie')
    parser.add_argument('--specific_idx', type=str, default='', help='Index of specific movies')
    parser.add_argument('--limit', type=int, default=-1, help='Page limitation for comments & best scripts')
    parser.add_argument('--sleep', type=float, default=0.1, help='Sleep time per each page in comments & best scripts')
    parser.add_argument('--casting', dest='casting', action='store_true')
    parser.add_argument('--bestscripts', dest='bestscripts', action='store_true')
    parser.add_argument('--comments', dest='comments', action='store_true')
    parser.add_argument('--debug', dest='debug', action='store_true', help='limit -> 3')
    parser.add_argument('--fast_update', dest='fast_update', action='store_true')

    args = parser.parse_args()
    directory = args.directory
    begin_idx = args.begin_idx
    end_idx = args.end_idx
    specific_idx = args.specific_idx
    limit = args.limit
    sleep = args.sleep
    casting = args.casting
    bestscripts = args.bestscripts
    comments = args.comments
    debug = args.debug
    fast_update = args.fast_update

    if debug:
        limit = 3

    for subdir in ['meta', 'actors', 'directors', 'staffs', 'bestscripts', 'comments']:
        path = '{}/{}/'.format(directory, subdir)
        if not os.path.exists(path) or os.path.isfile(path):
            os.makedirs(path)

    idxs = range(begin_idx, end_idx + 1)
    if specific_idx:
        idxs = [int(idx) for idx in specific_idx.split('_')]

    exceptions = []
    for idx in idxs:
        try:
            scrap(idx, directory, casting, bestscripts, comments, limit, sleep, fast_update)
        except Exception as e:
            print('movie id = {}'.format(idx))
            print(e)
            exceptions.append((idx, str(e)))
        if exceptions:
            print('Exist {} exceptions'.format(len(exceptions)))

    with open('./log', 'w', encoding='utf-8') as f:
        if not exceptions:
            f.write('Information of all movies were scraped successfully.\n')
        else:
            f.write('Exist exceptions\n\n')
            for idx, e in exceptions:
                f.write('movie id = {}'.format(idx))
                f.write('{}\n'.format(e))


if __name__ == '__main__':
    main()