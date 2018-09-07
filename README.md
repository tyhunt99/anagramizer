# Anagamizer

This package provides an API to perform simple operations on a dictionary of words related to anagrams. It also includes a module that manages the anagrams in such a way it can be expanded upon and used in other projects.

## Tech/framework used

* [Flask](http://flask.pocoo.org/docs/1.0/) - The web framework
* [pytest](https://docs.pytest.org/en/latest/) - Testing tool
* [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) - Code coverage tool
* [Docker](https://docs.docker.com/get-started/) - Containerization
* [gunicorn](https://gunicorn.org/#docs) - WSGI app for production
* [make](http://manpages.ubuntu.com/manpages/cosmic/man1/make.1.html) - Build scripting


## Getting Started
There are two methods to start the service:

### Docker Container

Requirements:
- docker (only tested on docker-ce 18.06.1-ce)

The simplest method is to run `make` which will build and start a container called anagramizer. It listens on 0.0.0.0:3000.

You can also run `make build` to simply build the container and start it with the configuration of your choice.

### Run on host

Requirements:

- python (only tested with python 3.6)
- virtualenv (recommended)

Setting up a virtualenv:
```bash
virtualenv --python=python3.6 .
source bin/activate
pip install -r requirements.txt
```
Then if running a production use gunicorn: `gunicorn --bind 0.0.0.0:3000 app` add `-D` to enable daemon mode
###### OR
Run in debug mode: `FLASK_ENV=development flask run`



## API Reference

### GET /

An endpoint to get a general summary of the entire corpus.

Example:
```bash
curl -i http://localhost:3000/
```

##### RESPONSE

HTTP/1.1 200 OK

###### BODY:
```json
{
  "stats": {
    "latest": true,
    "max": 4,
    "mean": 4,
    "median": 4,
    "min": 4,
    "num_words": 3,
    "top_anagrams": []
  },
  "words": [
    "dare",
    "dear",
    "read"
  ]
}
```


### POST /words.json

An endpoint to add a list of words to the corpus

Example:
```bash
curl -i -X POST -d '{ "words": ["read", "dear", "dare"] }' http://localhost:3000/words.json
```

###### BODY PARAMS
```json
{
  "words": [] # list of words to add to the corpus.
}
```

HTTP/1.1 201 Created



### DELETE /words.json

Delete all the words in the corpus.

Example:
```bash
 curl -i -X DELETE http://localhost:3000/words.json
```

##### RESPONSE
HTTP/1.1 204 No Content



### GET /anagrams/(word|string).json

Get all the anagrams in the dictionary for the specified word.

Example:
```bash
curl -i http://localhost:3000/anagrams/read.json?limit=1
```

###### PATH PARAMS
- word (string): word to find anagagrams

###### QUERY PARAMS
- limit (int): Limits the number of return anagrams to this value
- include_proper (bool): Whether to include proper nouns in returned anagams

##### RESPONSE

HTTP/1.1 200 OK

###### BODY:
```json
{
  "anagrams": [
    "dare"
  ]
}
```


### DELETE /anagrams/(word|string).json

Delete the word fromt the corpus

Example:
```bash
curl -i -X DELETE http://localhost:3000/anagrams/read.json
```

###### PATH PARAMS
- word (string): word to to remove from the corpus

##### RESPONSE

HTTP/1.1 204 No Content


### DELETE /anagams/(word|string)/delall

Delete a word and all its anagrams from the corpus.

Example:
```bash
curl -i -X DELETE http://localhost:3000/anagrams/read/delall
```

###### PATH PARAMS
- word (string): word to to remove from the corpus, and all its anagrams

##### RESPONSE

HTTP/1.1 204 No Content



### GET /anagrams/more/(size|int)

Get all anagram groups greater than or equal to size.

Example:
```bash
curl -i http://localhost:3000/anagrams/more/3
```

###### PATH PARAMS
- size (int): minimum size of anagram sets to return

##### RESPONSE

HTTP/1.1 200 OK

###### BODY:
```json
{
  "anagrams": [
    [
      "dare",
      "dear",
      "read"
    ]
  ]
}
```


### POST /anagrams/test

Test if a list of words are anagrams of each other.

Example:
```bash
curl -i -X POST -d '{ "words": ["read", "dear", "dare"] }' http://localhost:3000/words.json
```

###### BODY PARAMS
```json
{
  "words": [] # list of words to check
}
```

##### RESPONSE

HTTP/1.1 200 OK

###### BODY:
```json
{
  "anagrams": true
}
```


### GET /anagrams/stats

Example:
```bash
curl -i http://localhost:3000/anagrams/stats
```

##### RESPONSE

HTTP/1.1 200 OK

###### BODY:
```json
{
  "stats": {
    "latest": true,  # whether this stats are out of date with current corpus
    "max": 4, # Max word length in corpus
    "mean": 4,  # Mean word length in corpus
    "median": 4, # Median word length in corpus
    "min": 4, # Min word Length in corpus
    "num_words": 3 # Total number of words in corpus
  }
}
```

## Tests
Tests were run using pytest. To run the most basic test run ```pytest``` at the root project dir.

For full coverage report run:
```bash
 pytest --cov-report term-missing --cov anagramizer --cov app
```


## Development Notes
As I was developing this I had several thoughts which I will note here:

- Testing the API itself was slightly more difficult and felt like integration testing as opposed to unit testing. Especially when trying to build the initial state to be able to actually use some the endpoints under different conditions
- Versioning the API was something I struggled with. I could not come up with a decent way that wouldn't cause large amounts of spaghetti code in the future.
- I debated going with some sort of SQLLite on the back end for a data sstore since it is built in to python, but decided against because it seemed like overkill. Instead I simply store it to a file that can be either uncompressed or compressed with gzip.
- I had to find a vway to capture the service exiting in order to be sure and actually save the corpus to file so it is preserved on restart. Luckily python has a built in atexit which registers a function to be called on exit of the program. It currently does not catch the more abrupt signals.
- I did not to seem to have poor performance when using the provided dictionary, however more thorough testing of larger data sets would be needed to ensure scalability.
- I found it kind of difficult to actually document the end points in a consitent way that people would understand.


## Future Improvements

- Versioning for the api
- More paramterization in the api to allow more configuration
- Better testing of the api
- Testing of more versions of python
- Package the anagramizer package so it can be pip installed
- More robust build scripts
- Integrate testing and coverage output into CI/CD systems
- More robust backend data store to handle several requests, maybe NoSQL due to simple data structure
- More thorough error handling when not following the specified API docs


