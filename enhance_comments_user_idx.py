import argparse
import os
import time
from datetime import datetime
from naver_movie_scraper import save_list_of_dict
from naver_movie_scraper import scan_comment_indices
from naver_movie_scraper import scrap_comments_of_a_user


def check_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def make_indices_list(directory, debug):
    return sorted(scan_comment_indices(directory))

def save_index_list(indices, path):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(path, 'w', encoding='utf-8') as f:
        for idx in sorted(indices):
            f.write(f'{idx}\n')

def load_indices(path):
    with open(path, encoding='utf-8') as f:
        indices = [int(idx.strip()) for idx in f]
    return indices

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--comment_directory', type=str, default='./output/', help='Output directory')
    parser.add_argument('--enhanced_comment_directory', type=str, default='./user_comments/', help='Output directory')
    parser.add_argument('--index_list', type=str, default='./comment_indices', help='Remained comment indices')
    parser.add_argument('--sleep', type=float, default=0.1, help='Sleep time')
    parser.add_argument('--index_update_interval', type=int, default=100, help='Save index list per round')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Find indices from 10 movies')
    parser.add_argument('--noscrap', dest='noscrap', action='store_true', help='No scraip, only make index list')
    parser.add_argument('--force_make', dest='force_make', action='store_true', help='Remake index list if exist the index list file')

    args = parser.parse_args()
    directory = args.comment_directory
    data_dir = args.enhanced_comment_directory
    index_list = args.index_list
    sleep = args.sleep
    index_update_interval = args.index_update_interval
    debug = args.debug
    noscrap = args.noscrap
    force_make = args.force_make

    # load or make index list
    if (not os.path.exists(index_list)) or (force_make):
        indices = make_indices_list(directory, debug)
        save_index_list(indices, index_list)
    else:
        indices = load_indices(index_list)
    print(f'Found {len(indices)} indices')

    if noscrap:
        return None

    # scraping
    diff = n_indices = n_remains = len(indices)
    n_exceptions = 0
    n_rounds = 0

    exists = {}

    while indices and diff > 0:
        n_rounds += 1
        seed_idx = str(indices.pop())
        comments, n_exceptions_, flag, username, max_page = scrap_comments_of_a_user(seed_idx, sleep, exists)
        n_exceptions += n_exceptions_

        # update scraped user
        if max_page > 3:
            exists[username] = max_page

        dirname = f'{data_dir}/{seed_idx[:-4]}'
        check_dir(dirname)
        path = f'{dirname}/{seed_idx}'
        save_list_of_dict(comments, path)

        # integer
        removals = {c['idx'] for c in comments}
        print(removals)
        # integer
        indices = [idx for idx in indices if not (idx in removals)]

        # save remain indices
        if (n_rounds % index_update_interval == 0):
            save_index_list(indices, index_list)
            print('saved seed indices')
            time.sleep(1.0)

        diff = n_remains - len(indices)
        n_remains = len(indices)
        progress = 100 * (1 - n_remains / n_indices)
        now = str(datetime.now())[:19]
        print(f'\rscrap comments of a user ({progress:.4}%), -{diff} indices, {n_remains} remains, exceptions={n_exceptions} @ {now}')
        time.sleep(sleep)

    print('done')

if __name__ == '__main__':
    main()
