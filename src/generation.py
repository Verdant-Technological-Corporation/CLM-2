import random
from temps import *

subject = None


def apply_combos(tokens):
    if len(tokens) < 2:
        return tokens
    last_two = tuple(tokens[-2:])
    if last_two in combines:
        tokens[-2:] = [combines[last_two]]
    return tokens


def _filter_by_subject(options):
    global subject
    sub_options = {}
    for token_id, val in options.items():
        if len(val) >= 2:
            if val[1] == subject:
                sub_options[token_id] = val
        else:
            sub_options[token_id] = val
    return sub_options


def generate_next_token(tokens, autosub = False):
    global subject
    current_token = tokens[-1]
    
    options = None
    
    highest_available = max(temps_n.keys()) if temps_n else 0
    start_k = min(max_order, highest_available, len(tokens))
    
    for k in range(start_k, 0, -1):
        ctx = tuple(tokens[-k:])
        if ctx in temps_n.get(k, {}):
            options = temps_n[k][ctx]
            break
    
    if options is None:
        return None
    
    sub_options = _filter_by_subject(options)
    if not sub_options:
        sub_options = options
    
    token_ids = list(sub_options.keys())
    weights = [val[0] for val in sub_options.values()]
    penalized_weights = []
    
    for t, w in zip(token_ids, weights):
        word_str = id2word.get(t, "")
        
        if word_str == subject:
            penalized_weights.append(w)
        elif word_str in subjects:
            penalized_weights.append(0.0)
        elif t in tokens[-10:]:
            penalized_weights.append(w * 0.001)
        else:
            penalized_weights.append(w)
            
    if sum(penalized_weights) == 0.0:
        period_id = word_to_token(".")
        if period_id in token_ids:
            penalized_weights = [1.0 if t == period_id else 0.0 for t in token_ids]
        else:
            penalized_weights = [float(w) for w in weights]
    
    next_token = random.choices(token_ids, penalized_weights, k=1)[0]
    
    if current_token in subjects and autosub:
        subject = current_token
    
    return next_token

