import atexit
import os
import signal

from flask import (
    Flask, jsonify, request
)
from http import HTTPStatus

from anagramizer import Anagramizer

def create_app():
    app = Flask(__name__)

    def clean_up():
        '''
        A cleanup function to handle the exit of the service
        properly so the dictionary can be saved
        '''
        anagramizer.save_to_file('.dictionary_cache', compress=True)

    # root page which dumps the current corpus
    @app.route('/', methods=('GET',))
    def corpus():
        if not anagramizer.stats['latest']:
            anagramizer.calc_stats()
        return jsonify({
            'words': anagramizer.word_list(),
            'stats': anagramizer.stats,
        })

    @app.route('/words.json', methods=('POST',))
    def add_words():
        new_words = request.get_json(force=True)['words']
        for w in new_words:
            anagramizer.add_word(w)
        return (
            '',
            HTTPStatus.CREATED
        )

    @app.route('/words.json', methods=('DELETE',))
    def remove_all():
        anagramizer.remove_all()
        return ('', HTTPStatus.NO_CONTENT)

    @app.route('/anagrams/<string:word>.json', methods=('GET',))
    def get_anagrams(word):
        limit = int(request.args.get('limit', -1))
        include_proper = bool(request.args.get('include_proper', True))
        return (
            jsonify({'anagrams': anagramizer.get_anagrams(word, limit=limit, include_proper=include_proper)}),
            HTTPStatus.OK
        )

    @app.route('/words/<string:word>.json', methods=('DELETE',))
    def delete_word(word):
        # never differentiates between removing a word and a NOP
        anagramizer.remove_word(word)
        return ('', HTTPStatus.NO_CONTENT)

    @app.route('/anagrams/<string:word>/delall', methods=('DELETE',))
    def delete_all_word(word):
        anagramizer.remove_anagrams(word)
        return ('', HTTPStatus.NO_CONTENT)

    @app.route('/anagrams/top', methods=('GET',))
    def get_top_anagrams(word):
        return (
            '',
            HTTPStatus.NOT_IMPLEMENTED
        )

    @app.route('/anagrams/more/<int:size>', methods=('GET',))
    def greater_size_anagrams(size):
        anagrams = []
        for _, anagram_set in anagramizer._words.items():
            ana = list(anagram_set)
            app.logger.debug(ana)
            if len(anagram_set) >= size:
                anagrams.append(ana)
        return (
            jsonify({'anagrams': anagrams}),
            HTTPStatus.OK
        )

    @app.route('/anagrams/test', methods=('POST',))
    def test_anagrams(word):
        words = request.get_json(force=True)['words']
        return (
            jsonify({'anagrams': anagramizer.are_anagrams(words)}),
            HTTPStatus.OK
        )

    @app.route('/anagrams/stats', methods=('GET', 'POST',))
    def get_stats():
        if not anagramizer.stats['latest']:
            anagramizer.calc_stats()
        return (
            jsonify(anagramizer.stats),
            HTTPStatus.OK
        )

    return app


# grab the dictionary file otherwise assume it stored in cwd
dictionary_file = os.getenv('ANAGAMIZER_DICTIONARY', '.dictionary_cache.gz')

# initialize the corpus
anagramizer = Anagramizer(dictionary_file)

application = create_app()
atexit.register(anagramizer._save_to_file, dictionary_file, compress=True)
