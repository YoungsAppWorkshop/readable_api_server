# Readable: Python/Flask RESTful API server

[Readable](https://github.com/YoungsAppWorkshop/readable) is a content and comment web app built with React, and this is Python/Flask RESTful API server for the Readable app.

* Front-end Repository: [Readable](https://github.com/YoungsAppWorkshop/readable)
* 한글 리드미(README Korean) 파일: [README_ko.md](/README_ko.md)

## Demo
Demo Website URL: https://readable.youngsappworkshop.com

## How to Start

To start the Readable API server:

* Clone the project with `git clone https://github.com/YoungsAppWorkshop/readable_api_server`
* Change directory with `cd readable_api_server`
* Install and start the API server
  - `pip3 install -r requirements.txt`
  - `python3 run.py`

## Structure of the app
```bash
/readable_api_server
    /app
        __init__.py       # Application
        controllers.py    # API Blueprint
        models.py         # Database Schema
    ...
    config.py             # Configurations
    readable.db           # Sample database
    README.md
    run.py                # Python3 script to run the app
```

## API Endpoints

The following endpoints are available:

| Endpoints       | Usage          | Params         |
|-----------------|----------------|----------------|
| `GET /categories` | Get all of the categories available for the app. In the sample database, `"react"`, `"redux"`, or `"udacity"` are stored. |  |
| `GET /:category/posts` | Get all of the posts for a particular category. |  |
| `GET /posts` | Get all of the posts. Useful for the main page when no category is selected. |  |
| `POST /posts` | Add a new post. | **id** - UUID should be fine, but any unique id will work <br> **timestamp** - [Timestamp] Time in milliseconds. You can use `Date.now()` if you like. <br> **title** - [String] <br> **body** - [String] <br> **author** - [String] <br> **category** - path of the category. In the sample database, `"react"`, `"redux"`, or `"udacity"` are stored.|
| `GET /posts/:id` | Get the details of a single post. | |
| `POST /posts/:id` | Used for voting on a post. | **option** - [String]: Either `"upVote"` or `"downVote"`. |
| `PUT /posts/:id` | Edit the details of an existing post. | **title** - [String] <br> **body** - [String] |
| `DELETE /posts/:id` | Sets the deleted flag for a post to 'true'. <br> Sets the parentDeleted flag for all child comments to 'true'. | |
| `GET /posts/:id/comments` | Get all the comments for a single post. | |
| `POST /comments` | Add a comment to a post. | **id** - Any unique ID. As with posts, UUID is probably the best here. <br> **timestamp** - [Timestamp] Time in milliseconds. <br> **body** - [String] <br> **author** - [String] <br> **parentId** - Should match a post id in the database. |
| `GET /comments/:id` | Get the details for a single comment. | |
| `POST /comments/:id` | Used for voting on a comment. | **option** - [String]: Either `"upVote"` or `"downVote"`.  |
| `PUT /comments/:id` | Edit the details of an existing comment. | **timestamp** - [timestamp]. Time in milliseconds.<br> **body** - [String] |
| `DELETE /comments/:id` | Sets a comment's deleted flag to `true`. | &nbsp; |

## Attributions

This API server is built with [Flask](http://flask.pocoo.org/), [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/), [SQLAlchemy](https://www.sqlalchemy.org/),  [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/), and others. The API endpoints structure is inspired by [Udacity's Readable API Server repository](https://github.com/udacity/reactnd-project-readable-starter).

## License
[MIT Licensed](/LICENSE)
