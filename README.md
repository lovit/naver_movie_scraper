# 네이버 영화 정보 및 사용자 작성 영화평/평점 데이터 수집기

`naver_movie_scraper` 폴더는 다음의 파일들로 구성되어 있습니다.

| File | Note | Function |
| --- | --- | --- |
| basic.py | 메인 화면에서 영화 이름, 장르 등의 정보를 수집 | scrap_basic |
| comments.py | 사용자 작성 댓글과 평점을 수집 | scrap_comments |
| detail.py | 감독, 배우, 스탭 정보를 수집 | scrap_casting |
| script.py | 명대사를 수집 | scrap_bestscripts |
| utils.py | utils | get_soup<br>text_normalize<br>save_list_of_dict<br>load_list_of_dict |

영화 `라라랜드` 의 정보를 수집하는 예시로 사용법을 설명합니다. 라라랜드의 영화 아이디는 `134963` 입니다.

## scrap_basic

| Argument | Type | Note |
| --- | --- | --- |
| idx | int or str | 영화 아이디 |

```python
from naver_movie_scraper import scrap_basic

idx = 134963
scrap_basic(idx)
```

Return 값은 dict 형식입니다.

| Key | Type | Example value | Note |
| --- | --- | --- | --- |
| grade | str | '12세 관람가' | . |
| movie_idx | int | 134963 | . |
| title | str | '라라랜드' | . |
| e_title | str | 'La La Land , 2016' | 영어 제목에는 연도가 포함됨 |
| genres | list of str | ['멜로/로맨스', '뮤지컬', '드라마'] | 여러 개의 장르일 수 있음 |
| countries | list of str | ['미국'] | 여러 나라에서 공동 제작할 수 있음 |
| expert_score | float | 8.34 | 전문가 평점 |
| netizen_score | float | 8.9 | 네티즌이 작성한 장문의 리뷰 평균 평점 |
| open_date | list of str | ['2017-12-08', '2016-12-07'] | 재개봉 날짜가 포함될 수 있음 |
| running_time | int | 127 | . |
| story | str | 황홀한 사랑, 순수한 희망, 격렬한 열정... | 줄거리 |
| making_note | str | ABOUT MOVIE 1.<br>“이 영화는 마법이다”<br>올 겨울, 당신의 꿈이 이루어지는  ... | 매이킹 노트 |
| box_office | str | '3,598,929명(01.17 기준)' | 영화진흥위원회에서 제공하는 국내 관객 수 |

```
{'box_office': '3,598,929명(01.17 기준)'
 'countries': ['미국'],
 'e_title': 'La La Land , 2016',
 'expert_score': 8.34,
 'genres': ['멜로/로맨스', '뮤지컬', '드라마'],
 'grade': '12세 관람가',
 'making_note': 'ABOUT MOVIE 1.\n“이 영화는 마법이다”\n올 겨울, 당...',
 'movie_idx': 134963,
 'netizen_score': 8.9,
 'open_date': ['2017-12-08', '2016-12-07'],
 'running_time': 127,
 'story': '황홀한 사랑, 순수한 희망, 격렬한 열정…\n이 곳에서 모든...',
 'title': '라라랜드'}
```

## scrap_comments

| Argument | Type | Note |
| --- | --- | --- |
| idx | int or str | 영화 아이디 |
| limit | int | 명대사를 수집하는 페이지의 개수를 설정할 수 있습니다.<br>-1 이면 모든 페이지로부터 수집합니다.<br>기본값은 -1 입니다. |
| sleep | float | 과도한 데이터 수집은 서버에 부하를 줍니다.<br>sleep 은 수집하는 페이지마다 쉬는 간격입니다.<br>**sleep 을 작게 설정할 경우, 서버로부터 접근이 차단될 수 있습니다.**<br>여유가 되는대로 큰 값 (0.5 이상)으로 설정하십시요.|

```python
from naver_movie_scraper import scrap_comments

scrap_comments(idx, limit=3)
```

개봉 전, 개봉 후 영화 평 데이터를 모두 수집합니다. 수집 상황을 20 페이지 단위로 프린트 합니다.

```
movie 134963, after, 3 / 3 done
movie 134963, before, 3 / 3 done
```

Return 값은 list of dict 형식입니다.

| Key | Type | Example value | Note |
| --- | --- | --- | --- |

```
[{'agree': 0,
  'disagree': 0,
  'score': 10,
  'text': '꿈꾸는 모든 사람들, 그리고 그들과 삶의 화해를 위하여',
  'user': '15137658',
  'written_at': '2019.01.18 13:45'},
```

## scrap_casting

| Argument | Type | Note |
| --- | --- | --- |
| idx | int or str | 영화 아이디 |

```python
from naver_movie_scraper import scrap_casting

castings = scrap_casting(idx)
castings.keys()
```

Return 값은 list of dict 형식입니다. scrap_casting 의 return 값은 `actors`, `directors`, `staffs` 세 종류의 캐스팅 정보가 포함되어 있습니다.

```
dict_keys(['directors', 'actors', 'staffs'])
```

### actors

`actors` 는 배우 캐스팅에 관련된 정보입니다.

| Key | Type | Example value | Note |
| --- | --- | --- | --- |
| id | int | 5751 | . |
| k_name | str | '라이언 고슬링' | 한국 이름 |
| e_name | str | 'Ryan Gosling' | 영어 이름 |
| part | str | '주연' | 주연 혹은 조연 |
| role | str | '세바스찬 역' | 극중 역 이름 |
| casting_order | int | 1 | 숫자가 작을수록 영화 내에서 비중이 큰 역할 |

```python
scrap_casting(idx)['actors']
```

`라라랜드`의 두 주인공 `라이언 고슬링`과 `엠마 스톤`의 정보가 각각 dict 형태로 저장되어 있으며, 이들은 list 로 정렬되어 있습니다.

```
[{'cating_order': 1,
  'e_name': 'Ryan Gosling',
  'id': 5751,
  'k_name': '라이언 고슬링',
  'part': '주연',
  'role': '세바스찬 역'},
 {'cating_order': 2,
  'e_name': 'Emma Stone',
  'id': 135256,
  'k_name': '엠마 스톤',
  'part': '주연',
  'role': '미아 역'},
  ...
```

### directors

`directors` 는 감독 캐스팅에 관련된 정보입니다.

| Key | Type | Example value | Note |
| --- | --- | --- | --- |
| id | int | 175108 | . |
| k_name | str | '데이미언 셔젤' | 한국 이름 |
| e_name | str | 'Damien Chazelle' | 영어 이름 |

```python
scrap_casting(idx)['directors']
```

```
[{'e_name': 'Damien Chazelle', 'id': 175108, 'k_name': '데이미언 셔젤'}]
```

### staffs

`staffs` 는 스탭 혹은 우정출연 캐스팅에 관련된 정보입니다.

| Key | Type | Example value | Note |
| --- | --- | --- | --- |
| Key | Type | Example value | Note |
| id | int | 367641 | . |
| k_name | str | '저스틴 허위츠' | 한국 이름 |
| e_name | str | 'Justin Hurwitz' | 영어 이름 |
| role | str | '음악' | 영화의 역할로, 조연이 아닐 경우 제작, 음악, 기획 등의 값이 부여됨 |

```python
scrap_casting(idx)['staffs']
```

```
[{'e_name': '도로위 댄서', 'id': 395074, 'k_name': '레시마 게이자', 'role': ''},
 {'e_name': '유명한 여배우', 'id': 150418, 'k_name': '에이미 콘', 'role': ''},
 ...
 {'e_name': 'Fred Berger', 'id': 194407, 'k_name': '프레드 버거', 'role': '제작'},
 {'e_name': 'Gary Gilbert', 'id': 50303, 'k_name': '게리 길버트', 'role': '제작'},
 ...
 {'e_name': 'Justin Hurwitz', 'id': 367641, 'k_name': '저스틴 허위츠', 'role': '음악'},
 ...
]
```

## scrap_bestscripts

| Argument | Type | Note |
| --- | --- | --- |
| idx | int or str | 영화 아이디 |
| limit | int | 명대사를 수집하는 페이지의 개수를 설정할 수 있습니다.<br>-1 이면 모든 페이지로부터 수집합니다.<br>기본값은 -1 입니다. |
| sleep | float | 과도한 데이터 수집은 서버에 부하를 줍니다.<br>sleep 은 수집하는 페이지마다 쉬는 간격입니다.<br>**sleep 을 작게 설정할 경우, 서버로부터 접근이 차단될 수 있습니다.**<br>여유가 되는대로 큰 값 (0.5 이상)으로 설정하십시요.|

```python
from naver_movie_scraper import scrap_bestscripts

scrap_bestscripts(idx, limit=3)
```

list of dict 형식의 값을 return 합니다.

| Key | Type | Example value | Note |
| --- | --- | --- | --- |
| chracter | str | '세바스찬라이언 고슬링' | 대사의 주인공 |
| description | str | '우리 지금 어디 있는 거야?' | 사용자가 기술한 상황 혹은 메모 |
| num_agree | int | 403 | 사용자 동의 개수 |
| text | str | '그냥 흘러가는 대로 가보자.' | 영화 대사 |

```
[{'chracter': '세바스찬라이언 고슬링',
  'description': '기습심쿵♡.♡',
  'num_agree': 571,
  'text': '도서관 앞이라고 했잖아'},
 {'chracter': '세바스찬라이언 고슬링',
  'description': '미아 기다릴때 경적소리 ㅎㅎ',
  'num_agree': 405,
  'text': '빠아앙아앙아아아앙~~~'},
 {'chracter': '세바스찬라이언 고슬링',
  'description': '우리 지금 어디 있는 거야?',
  'num_agree': 403,
  'text': '그냥 흘러가는 대로 가보자.'},
  ...
 ]
```

## Script 를 이용한 데이터 수집

`script.py` 파일을 이용하면 위의 함수들을 모두 이용할 수 있습니다. 사용 가능한 arguments 는 아래와 같습니다.

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| directory | str | './output/' | Output directory |
| begin_idx | int | 134963 | Index of first movie |
| end_idx | int | 134963 | Index of last movie |
| specific_idx | str | '' | Index of specific movies<br>Under-bar separated idx<br>eg. 134963_10100 |
| limit | int | 3 | Page limitation for comments & best scripts |
| sleep | float | 0.1 | Sleep time per each page in comments & best scripts |
| casting | store_true | False | If use, scrap castings |
| comments | store_true | False | If use, scrap comments |
| bestscripts | store_true | False | If use, scrap best scripts |

```
python script.py --directory ./output/ --begin_idx 134963 --end_idx 134963 --specific_idx '' --limit 3 --sleep 0.1 --casting --comments --bestscripts
```

위 코드를 실행시키면 현재 폴더 아래 `output` 가 생성되며, 각각의 하위 폴더에 해당 정보들이 수집됩니다.

```
|-- output
    |-- actors
    |-- bestscripts
    |-- comments
    |-- directors
    |-- meta
    |-- staffs
```
