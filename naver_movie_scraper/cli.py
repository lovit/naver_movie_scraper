import argparse
import json
import os
import time
from tqdm import tqdm

from .basic import scrap_basic
from .detail import scrap_casting
from .script import scrap_bestscripts
from .comments import scrap_comments
from .utils import save_list_of_dict
from .utils import save_json
from .utils import load_list_of_dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, default='./output/', help='Output directory')
    parser.add_argument('--begin_idx', type=int, default=134963, help='Index of first movie')
    parser.add_argument('--end_idx', type=int, default=134963, help='Index of last movie')
    parser.add_argument('--specific_idx', type=str, nargs='+', default='', help='Index of specific movies')
    parser.add_argument('--limit', type=int, default=-1, help='Page limitation for comments & best scripts')
    parser.add_argument('--sleep', type=float, default=0.1, help='Sleep time per each page in comments & best scripts')
    parser.add_argument('--casting', dest='casting', action='store_true')
    parser.add_argument('--bestscripts', dest='bestscripts', action='store_true')
    parser.add_argument('--comments', dest='comments', action='store_true')
    parser.add_argument('--debug', dest='debug', action='store_true', help='limit -> 3')
    parser.add_argument('--fast_update', dest='fast_update', action='store_true')

    args = parser.parse_args()
    directory = args.output
    begin_idx = args.begin_idx
    end_idx = args.end_idx
    specific_idx = args.specific_idx
    limit = args.limit
    sleep = args.sleep
    debug = args.debug
    fast_update = args.fast_update

    if debug:
        limit = 3

    idxs = range(begin_idx, end_idx + 1)
    if specific_idx:
        idxs = [int(idx) for idx in specific_idx]

    n = len(idxs)
    exceptions = []

    os.makedirs(f'{directory}/meta/', exist_ok=True)
    for idx in tqdm(idxs, desc='Scrap basic meta', total=n):
        path = f'{directory}/meta/{idx}.json'
        if (fast_update) and (os.path.exists(path)):
            continue
        try:
            save_json(scrap_basic(idx), path)
        except Exception as e:
            exceptions.append(f'Scrap basic {idx}: {str(e)}')

    if args.casting:
        os.makedirs(f'{directory}/actors/', exist_ok=True)
        os.makedirs(f'{directory}/directors/', exist_ok=True)
        os.makedirs(f'{directory}/staffs/', exist_ok=True)
        for idx in tqdm(idxs, desc='Scrap casting', total=n):
            path = f'{directory}/actors/{idx}'
            if (fast_update) and (os.path.exists(path)):
                continue
            try:
                castings = scrap_casting(idx)
                for key in ['actors', 'directors', 'staffs']:
                    path = f'{directory}/{key}/{idx}'
                    if castings.get(key, []):
                        save_list_of_dict(castings[key], path)
            except Exception as e:
                exceptions.append(f'Scrap casting {idx}: {str(e)}')

    if args.bestscripts:
        os.makedirs(f'{directory}/bestscripts/', exist_ok=True)
        for idx in tqdm(idxs, desc='Scrap best-scripts', total=n):
            path = f'{directory}/bestscripts/{idx}'
            if (fast_update) and (os.path.exists(path)):
                continue
            try:
                scripts = scrap_bestscripts(idx, limit, sleep)
                if scripts:
                    save_list_of_dict(scripts, path)
            except Exception as e:
                exceptions.append(f'Scrap best-scripts {idx}: {str(e)}')

    if args.comments:
        os.makedirs(f'{directory}/comments/', exist_ok=True)
        for idx in tqdm(idxs, desc='Scrap comments', total=n):
            path = f'{directory}/comments/{idx}'
            last_time = None
            comments_ = []
            if fast_update and os.path.exists(path):
                comments_ = load_list_of_dict(path)
                last_time = comments_[0]['written_at']
            comments_new = scrap_comments(idx, limit, sleep, last_time)
            if comments_new:
                comments_ += comments_new
                comments_ = {json.dumps(obj, ensure_ascii=False) for obj in comments_}
                comments_ = [json.loads(obj) for obj in comments_]
                comments_ = sorted(comments_, key=lambda x:x['written_at'], reverse=True)
                save_list_of_dict(comments_, path)

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
