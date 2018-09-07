import gzip
import os

from statistics import median


class Anagramizer(object):

    def __init__(self, dictionary_file=None):
        self._words = {}
        self.stats = {}
        if dictionary_file and os.path.isfile(dictionary_file):
            _, ext = os.path.splitext(dictionary_file)
            print(ext)
            if ext == '.txt':
                with open(dictionary_file) as f:
                    for word in f:
                        self.add_word(word.rstrip('\n'))
            elif ext == '.gz':
                with gzip.open(dictionary_file, 'rb') as f:
                    for word in f:
                        self.add_word(word.decode().rstrip('\n'))
        self.calc_stats()

    def _word_exists(self, word):
        '''
        Helper function to determine if a word exists in the dictionary
        '''
        hash_key = ''.join(sorted(word.lower()))
        if hash_key in self._words.keys() and word in self._words[hash_key]:
            return True
        return False

    def _is_proper(self, word):
        '''
        Helper function to check and see if a given word is proper.
        Simply checks to see if first letter is capitalized.
        '''
        return word[0].isupper()

    def _save_to_file(self, file_path, compress=False):
        '''
        Saves the list ofwords to a simple sorted text file. Compress will
        cause it to be gzipped.
        Notes:
          - will always truncate file first
          - auto appends appropriate ext to file name
        '''
        if compress:
            with gzip.open(file_path, 'w') as f:
                f.write('\n'.join(self.word_list()).encode())
        else:
            with open(file_path, 'w') as f:
                f.write('\n'.join(self.word_list()))

    def word_list(self):
        '''
        Returns a list of all words currently in the dictionary
        as a sorted list using builtin sort.
        '''
        return sorted([w for a in self._words for w in self._words[a]])

    def remove_all(self):
        self._words = {}
        self.calc_stats()

    def add_word(self, word):
        hash_key = ''.join(sorted(word.lower()))
        if hash_key in self._words.keys():
            self._words[hash_key].add(word)
        else:
            self._words[hash_key] = set([word])
        self.stats['latest'] = False
        return True

    def remove_word(self, word):
        hash_key = ''.join(sorted(word.lower()))
        try:
            self._words[hash_key].remove(word)
            # also check if the set is empty and remove hash_key?
            self.stats['latest'] = False
            return True
        except KeyError:
            return False

    def remove_anagrams(self, word):
        hash_key = ''.join(sorted(word.lower()))
        try:
            del self._words[hash_key]
            return True
        except KeyError:
            return False

    def are_anagrams(self, words):
        '''
        Checks to see if a list of words are anagrams of each other
        '''
        # if not isinstance(words, list):
        #   raise TypeError('Expected list.')
        # if it is an empty list you can't have anagrams
        if not words:
            return False
        return len(list(set([''.join(sorted(word.lower())) for word in words]))) <= 1

    def get_anagrams(self, word, limit=-1, include_proper=True):
        anagrams = []
        hash_key = ''.join(sorted(word.lower()))
        try:
            # find the known anagrams and filter out uneeded
            anagrams = sorted([
                a for a
                in self._words[hash_key]
                if a != word and (include_proper or not self._is_proper(a))
            ])
            if limit >= 0:
                anagrams = anagrams[:limit]
        except KeyError:
            # the word is not known according to the current dictionary
            pass
        return anagrams

    def calc_stats(self):
        words = self.word_list()
        words_lengths = list(map(len, words))
        self.stats['num_words'] = len(words)
        self.stats['max']       = max(words_lengths) if len(words_lengths) else -1
        self.stats['min']       = min(words_lengths) if len(words_lengths) else -1
        self.stats['mean']      = int(sum(words_lengths)/len(words_lengths) if len(words_lengths) > 0 else -1)
        self.stats['median']    = median(words_lengths) if len(words_lengths) else -1
        # detemine the anagrams with most counts
        self.stats['top_anagrams'] = []
        self.stats['latest']    = True
