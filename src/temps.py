import os
import pickle
import gzip
import gc
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_PICKLE_PATH = os.path.join(_HERE, "temps.dat")

try:
    with gzip.open(_PICKLE_PATH, "rb") as _f:
        _data = pickle.load(_f)
except FileNotFoundError as _e:
    print("Cant find.")

word2id = _data["word2id"]
id2word = _data["id2word"]
temps_n = _data["temps_n"]
combines = _data["combines"]
subjects = _data["subjects"]
max_order = _data["max_order"]


def words_to_tokens(words):
    tokens = []
    for word in words:
        if word in word2id:
            tokens.append(word2id[word])
        else:
            tokens.append(None)
    return tokens


def tokens_to_words(tokens):
    words = []
    for token in tokens:
        if token is None:
            words.append(None)
        elif token in id2word:
            words.append(id2word[token])
        else:
            pass
    return words


def word_to_token(word):
    return word2id.get(word, None)


def token_to_word(token):
    return id2word.get(token, f"<UNK:{token}>")

_data = None
gc.collect()

if sys.platform.startswith("linux"):
    import ctypes
    
    try:
        libc = ctypes.CDLL("libc.so.6")
        libc.malloc_trim(0)
    except Exception:
        pass
