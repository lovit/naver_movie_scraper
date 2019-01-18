import argparse
import os
import time

from naver_movie_scraper import scrap_basic
from naver_movie_scraper import scrap_casting
from naver_movie_scraper import scrap_bestscript
from naver_movie_scraper import scrap_comments
from naver_movie_scraper import save_list_of_dict
from naver_movie_scraper import save_json


def scrap(idx, directory, casting=True, bestscripts=True, comments=True, limit=3, sleep=0.05):
    # basic
    save_json(scrap_basic(idx), '{}/meta/{}.json'.format(directory, idx))
    print('scraped {} basic'.format(idx))

    # castings
    if casting:
        castings = scrap_casting(idx)
        for key in ['actors', 'directors', 'staffs']:
            if castings.get(key, []):
                save_list_of_dict(castings[key], '{}/{}/{}'.format(directory, key, idx))
        print('scraped {} casting'.format(idx))

    # best scripts
    if bestscripts:
        scripts = scrap_bestscript(idx, limit, sleep)
        if scripts:
            save_list_of_dict(scripts, '{}/bestscripts/{}'.format(directory, idx))
        print('scraped {} best scripts'.format(idx))

    # comments
    if comments:
        comments_ = scrap_comments(idx, limit, sleep)
        if comments_:
            save_list_of_dict(comments_, '{}/comments/{}'.format(directory, idx))
        print('scraped {} comments'.format(idx))

    print('')
    time.sleep(sleep)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, default='./output/', help='Output directory')
    parser.add_argument('--begin_idx', type=int, default=134963, help='Index of first movie')
    parser.add_argument('--end_idx', type=int, default=134963, help='Index of last movie')
    parser.add_argument('--specific_idx', type=str, default='', help='Index of specific movies')
    parser.add_argument('--limit', type=int, default=3, help='Page limitation for comments & best scripts')
    parser.add_argument('--sleep', type=float, default=0.1, help='Sleep time per each page in comments & best scripts')
    parser.add_argument('--casting', dest='casting', action='store_true')
    parser.add_argument('--bestscripts', dest='bestscripts', action='store_true')
    parser.add_argument('--comments', dest='comments', action='store_true')

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
            scrap(idx, directory, casting, bestscripts, comments, limit, sleep)
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