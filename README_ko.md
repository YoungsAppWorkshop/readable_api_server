# Readable: Python/Flask RESTful API server

[Readable](https://github.com/YoungsAppWorkshop/readable/blob/master/README_ko.md)은 리액트(React)를 활용하여 제작된 컨텐츠 및 댓글 작성 앱입니다. 이 서버는 `Readable`앱을 위하여 파이썬(Python)/플라스크(Flask) 프레임워크로 제작된 RESTful API 서버입니다.

* 프론트엔드 깃허브 저장소: [Readable](https://github.com/YoungsAppWorkshop/readable/blob/master/README_ko.md)
* 영문 리드미(English README) 파일: [README.md](/README.md)

## 데모
데모 웹사이트 URL: https://readable.youngsappworkshop.com

## 설치 방법

API 서버를 시작하기 위해:

* GitHub 저장소 복제합니다: `git clone https://github.com/YoungsAppWorkshop/readable_api_server`
* 프로젝트 디렉토리로 이동합니다: `cd readable_api_server`
* 필요한 패키지를 설치하고 서버를 시작합니다.
  - `pip3 install -r requirements.txt`
  - `python3 run.py`

## 어플리케이션 구조
```bash
/readable_api_server
    /app
        __init__.py       # 어플리케이션(Application)
        controllers.py    # API 블루프린트(Blueprint)
        models.py         # 데이터베이스 스키마 정의
    ...
    config.py             # 설정 파일
    readable.db           # 견본 데이터베이스
    README.md
    run.py                # 서버 시작 스크립트
```

## API 엔드포인트

아래의 API 엔드포인트를 활용할 수 있습니다:

| Endpoints       | Usage          | Params         |
|-----------------|----------------|----------------|
| `GET /categories` | 모든 카테고리를 반환. 견본 데이터베이스에는 `"react"`, `"redux"`, `"udacity"`가 저장되어 있음.|  |
| `GET /:category/posts` | 특정한 카테고리의 모든 포스트를 반환. |  |
| `GET /posts` | 모든 카테고리의 모든 포스트를 반환. |  |
| `POST /posts` | 새로운 포스트를 생성. | **id** - 고유 아이디(ex. UUID 등)<br> **timestamp** - [Timestamp] Time in milliseconds. `Date.now()`를 사용 가능. <br> **title** - [String] <br> **body** - [String] <br> **author** - [String] <br> **category** - 특정 카테고리의 `path` |
| `GET /posts/:id` | 특정한 포스트의 정보를 반환. | |
| `POST /posts/:id` |포스트에 '좋아요' 또는 '싫어요' 투표 시 사용. | **option** - [String]: `"upVote"` 또는 `"downVote"` |
| `PUT /posts/:id` | 특정한 포스트를 수정. | **title** - [String] <br> **body** - [String] |
| `DELETE /posts/:id` | 특정한 포스트의 `deleted` 플래그를 `true`로 설정. <br> 그 포스트의 모든 댓글의 `parentDeleted` 플래그를 `true로 설정'. | |
| `GET /posts/:id/comments` | 특정한 포스트의 모든 댓글을 반환.| |
| `POST /comments` | 특정한 포스트에 댓글을 생성.| **id** - 고유 아이디(ex. UUID 등) <br> **timestamp** - [Timestamp] Time in milliseconds. `Date.now()`를 사용 가능. <br> **body** - [String] <br> **author** - [String] <br> **parentId** - 포스트의 `id`와 반드시 일치해야 함.|
| `GET /comments/:id` | 특정한 댓글의 정보를 반환. | |
| `POST /comments/:id` | 댓글에 '좋아요' 또는 '싫어요' 투표 시 사용. | **option** - [String]: `"upVote"` 또는  `"downVote"`.  |
| `PUT /comments/:id` | 특정한 댓글을 수정. | **timestamp** - [timestamp]. Time in milliseconds. <br> **body** - [String] |
| `DELETE /comments/:id` | 특정한 댓글의 `deleted` 플래그를 `true`로 설정. | &nbsp; |

## 참고자료
이 API 서버는 [Flask](http://flask.pocoo.org/), [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/), [SQLAlchemy](https://www.sqlalchemy.org/),  [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/) 등의 라이브러리를 활용하여 제작되었습니다. API 엔드포인트의 구조는 [유다시티의 Readable API 서버 저장소](https://github.com/udacity/reactnd-project-readable-starter) 코드를 참조하였습니다.

## 라이센스
[MIT 라이센스](/LICENSE)
