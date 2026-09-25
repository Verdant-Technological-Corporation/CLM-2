from temps import *
from generation import *
import random

# Build Info
debug = False
version = "2.0.0"
status = "alpha"

if debug:
    random.seed(int(input("Seed: ")))


def tokens_to_sentence(tokens):
    if tokens[0] is None:
        return "Soft Error: End of sentence as first token"
    
    words = tokens_to_words(tokens)
    
    result = words[0] if words[0] else ""
    skip_next = True
    
    for word in words[1:]:
        if skip_next:
            skip_next = False
            continue
        if word is None:
            result += "."
            break
        result += " " + word
    
    return result


while True:
    try:
        user_input = input(">> ").strip()
        
        if not user_input:
            continue
        
        input_words = user_input.split(" ")
        
        tokens = []
        for word in input_words:
            word = word.strip().lower()
            if word in word2id:
                tokens.append(word2id[word])
            else:
                continue
        
        if not tokens:
            print("Err")
            continue
        
        current_token = tokens[-1]
        while current_token is not None:
            next_token = generate_next_token(tokens, True)
            tokens.append(next_token)
            tokens = apply_combos(tokens)
            current_token = tokens[-1]
        output = tokens_to_sentence(tokens)
        print(output)
    except:
        print("Err")
